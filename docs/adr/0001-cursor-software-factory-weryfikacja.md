# ADR-0001: Cursor jako software factory — weryfikacja źródeł i ustawienie

**Status:** przyjęta  
**Data:** 2026-08-31  
**Moduły:** platforma (M-68+), wszystkie  
**Plan Cursor:** `.cursor/plans/cursor_software_house_84d0f6a6.plan.md` (lokalnie w IDE)

## Kontekst

OmniRoute budowany jest przez 1 operatora + agenty AI, z metaforą **~30 ról software house**, przy zachowaniu kodu „jak od człowieka”. Materiały wejściowe:

- 60+ plików MD w `Informacje z claude/` (PLAN-GLOWNY, AGENTS-v2, KIT, ZESTAW, aneksy)
- [Consensus — modułowe ERP z AI transportu](https://consensus.app/search/modułowe-erp-z-ai-transportu/KQ2VE-DzSsyfHgrDQMsnZg/)
- [Audyt Gemini PDF](../Informacje%20z%20claude/Audyt%20architektury%20AI%20dla%20ERP%20-%20Google%20Gemini.pdf) (archiwum)
- [ChatGPT share — Ocena repozytoriów / systemdesign](https://chatgpt.com/share/6a95817e-bbac-83eb-96b1-26528a80fa44)

Pytanie: czy obecne ustawienie Cursor jest optymalne, czy da się lepiej zaplanować i przeprowadzić konfigurację?

---

## §0 Werdykt weryfikacji (31.08.2026)

### Źródła naukowe i eksperckie użyte w triangulacji

| Źródło | Wkład |
|---|---|
| Treude & Baltes 2026 (context rot) | Stale refs w ~23% repo z plikami AI-config |
| Palmblad et al. 2026 (GROUNDING.md) | HC/CP — odmowa vs ostrzeżenie |
| Galster et al. 2026 | AGENTS.md jako standard; praktyki konfiguracji agentów |
| Gloaguen / ETH Zurich 2026 | Auto-AGENTS: −3% success, +20% koszt; human-curated lekko + |
| arXiv 2606.26924 (deterministic control plane) | Hooks, HITL, integrity, cap na rekursję agentów |
| Morph / Cursor Rules 2026 | alwaysApply łącznie < ~2k tokenów |
| CSA README injection 2025 | Ryzyko zatrucia `.cursor/rules`, agentlint |
| Consensus (modułowe ERP) | Spec-driven, AGENTS+Skills+GROUNDING, modular monolith |
| Gemini audyt | Context poisoning, taśma deterministyczna, Module Factory |
| ChatGPT systemdesign | Knowledge Library, artefakty zamiast agent-chat |

### Co NOWE źródła potwierdzają (plan zostaje / wzmacniamy)

| Teza | Gemini | ChatGPT | Nauka/eksperci | Decyzja |
|---|---|---|---|---|
| 500×Rules/Skills w kontekście = context poisoning | Tak | Tak | Treude; Morph | **≤3 alwaysApply**; reszta globs/Skills |
| Multi-agent „zebranie” pogarsza jakość | Tak | Tak | error propagation | **Taśma artefaktów**, nie chat agent↔agent |
| Rules ≠ Skills ≠ Tools | Tak | Tak | Cursor docs 2026 | Czysty podział ról |
| LLM extract → kod waliduje/liczy/zapisuje | Tak | Tak | AGENTS-v2 zasady 4–8 | **GROUNDING.md** + zero write-AI |
| Modular monolith + Temporal | Tak | Tak | REWIZJA-STOSU | FastAPI + Temporal + Vite |
| Knowledge poza kontekstem + retrieval 8–20 | Częściowo | Tak | RAG tylko na nieustrukturyzowane | `docs/_knowledge/` + skill `knowledge-retrieve` |

### Przyjęte ulepszenia z Gemini/ChatGPT

1. **Knowledge Library** — wzorce poza always-context; max 8–20 kart na zadanie.
2. **Module Factory** — matryca modułu: schemas + service + api + opcjonalnie ai_transforms.
3. **`ui-design-system.mdc`** — anti-AI-slop, data density.
4. **Zero Write Autonomia** — AI = intent; zapis przez service + HITL.
5. **Integrity instrukcji** — agentlint + `check_agent_refs.py` w CI.
6. **Komunikacja przez artefakty** — delta-spec, ADR, OpenAPI, raport testów.

### Świadomie odrzucone

| Propozycja | Źródło | Powód |
|---|---|---|
| Pełny Event Sourcing | Gemini | Kanon: outbox + audit_log |
| NestJS/Next primary | Gemini | OCR/analityka → Python; app = Vite SPA |
| Turborepo/Nx obowiązkowo | Gemini | import-linter wystarczy na start |
| 30 person agentów | ChatGPT (wczesna rada) | Korekta w tej samej rozmowie; REWIZJA odrzuca |
| Dump 2×200 repo / 1000 kart do kontekstu | User + oba źródła | Context poisoning |
| RAG na logikę wyceny / schemat DB | Gemini | HC-08 w GROUNDING.md |

### Werdykt vs pierwotny plan Cursor

**Kierunek był właściwy (~85%).** Nowe źródła **nie zmieniają stosu ani WIP=1**, lecz zaostrzają anty-poisoning i formalizują software factory.

---

## Weryfikacja końcowa: czy można LEPIEJ?

**Odpowiedź: tak — marginalnie, w wykonaniu i kuracji, nie w przebudowie architektury Cursor OS.**

Obecny stack (AGENTS.md + GROUNDING.md + cienkie Rules + Skills on-demand + Hooks + CI + delta-spec + WIP=1) jest **zgodny z najlepszą praktyką 2025–26** i nie wymaga alternatywnego „frameworka Cursor”. Badania nie wskazują lepszego modelu niż: **cienki kontekst deklaratywny + twarde bramki deterministyczne + spec przed kodem**.

### Co już robimy dobrze (nie zmieniać)

| Element | Uzasadnienie eksperckie |
|---|---|
| AGENTS.md ≤130 linii, human-written | ETH Zurich: unikaj auto-AGENTS; Red Hat: nie shipuj `init` as-is |
| GROUNDING.md jako HC | Palmblad: warstwa odmowy ponad prompt |
| ≤3 alwaysApply rules | Morph: budżet tokenów; mniej rot |
| Skills zamiast procedur w Rules | Context engineering: deklaratywne > proceduralne (mniej rot) |
| Hooks + `just gate` | Gemini taśma; arXiv: deterministyczna kontrola |
| WIP=1 + delta-spec | Mniej sprzecznych instrukcji niż równoległe agenty |
| `no-slop.mdc` + jscpd | Kashif-class: Type-4 clones w kodzie AI |
| Archiwum MD poza kontekstem | 60+ plików nigdy naraz — tylko kompilacja do `docs/spec/` |

### Rekomendowane ulepszenia wykonania (kolejność)

| # | Ulepszenie | + | − | Alternatywa | Dlaczego to wybieramy |
|---|---|---|---|---|---|
| 1 | **Nested `AGENTS.md` per BC** (`backend/app/domains/<bc>/`) | Kontekst JIT, mniej tokenów | Więcej plików do utrzymania | Jeden gruby AGENTS | Galster/Treude: scope per bounded context |
| 2 | **Golden exemplars** — 1–2 moduły wzorcowe w repo po plasterze 0.3 | Agent kopiuje styl człowieka | Czas na dopracowanie wzorca | Same rules bez przykładu | Badania: reviewer undervalues semantic clones — wzorzec > opis |
| 3 | **agentlint w CI** (obowiązkowo) | Ochrona przed injection w rules | False positives | Ręczny review rules | CSA 2025 |
| 4 | **Nie wymieniać wszystkich MCP w AGENTS.md** | Unika 2.5× overuse narzędzi (ETH) | Agent musi czytać mcp.json | Długa lista tooli w AGENTS | Context engineering best practices |
| 5 | **Kompilacja MD → spec/** partiami (nie „całe archiwum”) | Jedno źródło prawdy bez poisoning | Praca redakcyjna | @Informacje z claude w każdym czacie | Gemini + ChatGPT + własny AUDYT poziom C |
| 6 | **Piątkowa retrospektywa rules/hooks** (15 min) | Usuwanie rot; +23% compliance w badaniach reguł | Czas operatora | Nigdy nie czyścić | Cai 2026 rule evolution |
| 7 | **Metryka „kod jak człowiek”** | transferred/added ≥10%, jscpd ≤3%, cov ≥80% | Wymaga dyscypliny | Subiektywny „wygląda OK” | Mierzalne, egzekwowane w gate |
| 8 | **Testy domenowe pisze człowiek** (skill testolog tylko szkielet) | Mniej fałszywego green | Wolniej | AI pisze testy i kod | Claude Consensus + Wasza zasada |

### Czego NIE robić (potwierdzone wszystkimi źródłami)

- Nie ładować `Informacje z claude/` hurtowo do kontekstu.
- Nie generować AGENTS.md / rules LLM-em „na całość”.
- Nie uruchamiać 30 subagentów-person równolegle.
- Nie zastępować hooks „prośbą w prompcie”.
- Nie używać Memories Cursor na pipeline cenników.

---

## Decyzja

1. **Przyjmujemy** obecną architekturę Cursor OS (Phase A) jako kanoniczną.
2. **Uzupełniamy** ją o ulepszenia #1–#8 powyżej w Fazach B–D (priorytet: golden exemplar po 0.3, agentlint w CI, nested AGENTS per BC).
3. **Archiwum** `Informacje z claude/` traktujemy jako **materiał źródłowy do kompilacji**, nigdy jako kontekst sesji.
4. **Metafora 30 osób** = 6 powierzchni procesu + efemeryczne subagenty review/QA, **nie** 30 chatujących person.

---

## Rozważane alternatywy

| Alternatywa | Dlaczego odrzucona |
|---|---|
| 500 reguł/promptów w Cursorze | Context poisoning (Gemini, ChatGPT, Treude) |
| Pełny RAG na całe repo MD | Gubi typy i powiązania AST; zakaz na logikę (HC-08) |
| Cursor-only bez GitHub/CI | Brak audytu; „dyscyplina nie działa, działa CI” |
| Zespół person CEO/CFO/PM w promptach | REWIZJA-BADAWCZA odrzuca; ChatGPT sam koryguje |
| Microservices / Nx monorepo day-1 | DECISIONS: modular monolith |

---

## Konsekwencje

- **Pozytywne:** Powtarzalna jakość, audytowalność, zgodność z badaniami, kod bliżej „ludzkiego” przez bramki nie przez persony.
- **Negatywne:** Narzut ~15 min/plaster (delta-spec); kuracja `_knowledge/` i kompilacja spec wymaga czasu operatora.
- **Następne kroki (produkt):** plaster **0.10** langfuse / promptfoo CI.
  0.3 jest golden exemplar (zarchiwizowany). `agentlint` już w `just gate`.

---

## Powiązane artefakty w repo

| Plik | Rola |
|---|---|
| `AGENTS.md` | Kontrakt agenta (≤130 linii) |
| `GROUNDING.md` | Hard Constraints domenowe |
| `.cursor/rules/` | JIT + alwaysApply |
| `.cursor/skills/` | Procedury SH on-demand |
| `docs/_knowledge/` | Biblioteka wzorców (retrieve, nie dump) |
| `docs/spec/` | Skompilowane specy modułów (<400 linii) |
| `Informacje z claude/` | Archiwum źródłowe — **nie ładować do agenta** |
