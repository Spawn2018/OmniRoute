# Briefing dla Claude — OmniRoute software house

**Data:** 2026-09-02  
**Cel tego pliku:** jeden pakiet dla Claude (analiza, poprawa, zabezpieczenie, rozszerzenie, **bezpieczna** automatyzacja). Nie jest kanonem produktu. Kanon: `docs/PLAN-REALIZACJA.md`, `docs/state/CURRENT.md`, `GROUNDING.md`, `AGENTS.md`.

**Canvasy (lokalnie, poza gitem):**

- [Audyt wydmuszek](C:/Users/sebas/.cursor/projects/d-OMNIROUTE/canvases/moduly-wydmuszki-audyt.canvas.tsx)
- [Zakres po planie](C:/Users/sebas/.cursor/projects/d-OMNIROUTE/canvases/zakres-po-planie.canvas.tsx)
- [Software house Cursor](C:/Users/sebas/.cursor/projects/d-OMNIROUTE/canvases/software-house-cursor.canvas.tsx)

**DNA wizualne (produkt):** `docs/design/omniroute-ui.html` — hue 165, s1–s6, radius 12px/8px, IBM Plex. Tokeny w `frontend/src/index.css`.

**Mockup briefingu (nie paleta):** `docs/design/omniroute-briefing-mockup.html`. Opis prompta: §6 (dopisek) + §8.

**Ograniczenie źródeł:** `Informacje z claude/` i `docs/_source/` są w `.cursorignore` i `excludePatterns`. Audyt nie dumpował 60+ MD ani PDF Gemini z dysku. Wkład Gemini/Claude/nauki wzięty z `docs/adr/0001-cursor-software-factory-weryfikacja.md` (cytuje PDF Gemini, ChatGPT share, Consensus, Treude 2026, ETH Auto-AGENTS, Palmblad GROUNDING, CSA 2025).

---

## 1. Stan produktu (skrót audytu kodu)

54/70 slotów M-01…M-70 ma żywą powierzchnię. **Nie są to puste stuby.** Warstwy:

| Warstwa | Ile | Co jest | Czego nie ma |
|---|---|---|---|
| Katalog BC | 18 | Tabela, RLS, POST, UI katalogu | Silnik procesu |
| Matcher M-11 | 1 | `resolve_email` | IMAP |
| Nakładki `/quotations` | 8 | Panele JS + batch POST | Własna tabela |
| Tablice-odczyt | 27 | Trasa + filtr cudzego API | Serwis, tabela, zapis |
| Poza produktem | 16 | M-02 parked, M-04 częściowe OpenFGA, M-17/22 COVERED, M-54/55/58–67 | — |

Backend: 15 pakietów `services`, 24 routery, ~28 tabel RLS. Frontend: 47 tras `BUSINESS_LISTS`. `ARCHITECTURE.md` ten rozjazd dokumentuje.

**CURRENT (2026-09-02):** Fala S, następny **64.0 S1 `/plaster`** — `inbound_message` + draft + fixture. Nie Graph, nie IMAP, nie send, nie shipment.

---

## 2. Co zostanie po realizacji planu (S1–S59 + wpinanie 71–212)

Plan **zdejmuje po jednym „nie X”**. Nie zamienia tablicy w pełny produkt o nazwie z archiwum.

### 2.1 Mocny zakres (kręgosłup E2E)

M-01+M-04 (Auth0 S53), M-20 (mail→HITL→`rate_line`), M-21+M-28 (RFQ→wycena SQL), M-08 (`charge` = marża, spread S22), M-32 (skrzynka S1/S15/S17), **S11+S14** (szyna Akceptuj/Zmień + lock — **nowy żywy ID, nie M-57**), M-33 (wysyłka po SOP S18), M-35+S32 (shipment + Watchtower), M-40+S35 (FV + KSeF osobno), M-02 (outbox S16), M-16+S10 (SOP „kiedy nie wolno auto”).

Nadal nie: czat, auto-zapis stawek, auto-send, mapa w initial JS, Temporal-teatr, drugi silnik marży.

### 2.2 Średni zakres

Geografia, katalogi kodów/NBP/DG, party (+ GUS gdy klucz — leftover), `network_member`, fakty ryzyka/kredyt/karta, finance board z FV, `applies_when` SQL, live kanał **przy umowie**, won/lost, dokument oferty, notices, tracking eventy, dokumenty, EDI **gdy partner**, finanse M-41…47, nogi M-48…51, sankcje HTTP, RODO wniosek, OTel.

### 2.3 Słaby zakres / wydmuszka po planie

- **S55 paczka** M-61…67 — siedem portali w jednym wierszu; giełda live tylko przy umowie.
- M-19 bez umowy, M-39 bez partnera, M-50 HTTP korytarza, M-111 flota „tylko gdy auta” → **named park**, nie teatr.
- M-27 CSV z boku. M-33 ≠ Office.js. M-57…60: nie nowy czat; LLM nie liczy; nigdy auto-przelew/send/booking.
- M-54/55/76/91: jeden plaster katalogowy.
- M-69/70: QA i rollout ≠ billing SaaS.
- Watchtower mapa = lazy chunk (canvas ui-06).

### 2.4 Braki, których plan nie domyka

| Brak | Wolno? |
|---|---|
| Katalog 71–212 (cło, WMS, A/B, C na końcu, fintech 207–208 ostatnie) | Wpinane gdy poprzednik; nie od 71 w górę |
| M-203, M-204 puste | Nie zgaduj nazwy |
| Presidio + llm-guard na każdym endpoincie | Cel HC, osobne plastry; dziś guard regex + Presidio stub |
| p95 50k / k6 | Gdy są wiersze; 61.0 = N/A przy 0 |
| Live GUS/VIES/NBP/NGA | Gdy operator ma klucz; CI = fixture |
| OpenFGA tuple per party | Leftover 5.0; `can_*` ≠ member |
| Temporal/Hatchet | Dopiero po realnym zdarzeniu między BC (outbox S16 pierwszy) |
| pgvector, Infisical, Next, 70 stubów, scoring osoby | **Anty-cele — nie robić** |
| Auto-AGENTS / dump archiwum / RAG na wycenę | Odrzucone ADR-0001 |

### 2.5 Trwałe zasady (nie „dowieźć planem”)

LLM nie liczy. HITL przed stawką. `charge` = marża. `rate_line` niemutowalna + `source_ref`. Auto-send/booking/przelew zakazane. Scoring `natural_person`/JDG zakazany. COVERED: nie drugi M-17/M-22.

### 2.6 Jak zapełniać (pomysły — Gemini/ADR/leftover/canvas/PLAN)

**Mocny:** how-to per job (wzorzec 62.0); Watchtower S32 + HITL, mapa lazy poza 250 kB; set-based batch gdy p95 boli (leftover 20.0); KSeF jako sieć prawna; outbox tylko na zdarzenie.

**Średni:** GUS/VIES gdy klucz; NBP HTTP bez `amount * mid`; `pg_trgm` na port; zapis `location.kind`; tuple OpenFGA; S21 tylko z umową; S27 przed bookingiem.

**Słaby:** rozbić S55 na osobne Plan+plaster per portal; CURRENT „parked aż umowa”; 71–212: cło/WMS po shipment+dokumentach; M-203/204 puste aż człowiek nazwie.

Źródła pomysłów: PLAN § Fala S, `docs/ops/docs-debt.md`, canvas `kolejka-s-poglebien` / `ui-06-vision` / `omniroute-12m-plan`, ADR-0001, `docs/ops/threat-model-tenant-hitl.md`, `docs/operator/*`.

---

## 3. Architektura software house w Cursorze (jak jest)

### 3.1 Werdykt

Taśma jest dojrzała (spec → testy → kod → karta jakości → gate → push). **Uczenie się nie jest zaplanowane jako pętla.** Cursor Automations = 0. Auto-przepis `AGENTS.md` jest zakazany (ETH: −3% success, +20% koszt).

Metafora ~30 ról = komendy + jeden subagent, nie 30 czatów. Kanon nazw: komenda testów → `/testy`; komenda bramki → `/bramka`; zamknięcie plastra → `zamknij-plaster`.

### 3.2 Warstwy sterowania (twarde → miękkie)

1. **GROUNDING.md** — HC wygrywają z promptem (RLS, Decimal, HITL, sekrety, idempotencja, SQL nie z LLM na wycenę).
2. **AGENTS.md ≤130** — stos, 13 zasad, pionowy plaster, DoD vs echo. Nested `AGENTS.md` per BC (już w `services/*`).
3. **alwaysApply (≤3):** `context.mdc`, `no-slop.mdc`, `security-tenancy.mdc`.
4. **globs:** backend, frontend, testing, database, performance, workflows (Temporal **cel**, pliki `workflows/**`), ui-design-system.
5. **Komendy (9):** `plan-modul`, `plaster`, `testy`, `bramka`, `zamknij`, `noc`, `delta`, `po-plastrze`, `refaktor`.
6. **Skills repo:** nowy-plaster, zamknij-plaster, migracja-rls, module-factory (zakaz 70 stubów), ekstraktor, openfga-change, pr-review, refaktor-pass, knowledge-retrieve, lowca-duplikatow.
7. **User skills-cursor (prawie poza taśmą):** automate, loop (tylko `/noc`), canvas, bugbot, security-review, create-hook/rule/skill, split-to-prs, goals, autopilot, origin, statusline.
8. **Subagent:** tylko `.cursor/subagents/lowca-duplikatow.md`. Zakaz person w `.cursor/agents/`.
9. **Hooks:**  
   - `beforeSubmitPrompt` → `pre_edit.py` (weto: `frontend/src/api/`, archived deltas, `.cursor/hooks/`, ADR, archiwum Claude, applied alembic).  
   - `afterFileEdit` → ruff/mypy lub prettier+tsc.  
   - `stop` → sync OS status, lint-imports, jscpd, vulture (`FileNotFoundError` = skip).
10. **settings.json:** autoReview allowlista `just`/`pytest`; `requireApproval` push/commit/docker/curl/rm/downgrade/`just gate`; exclude archiwum Claude, `_source`, wygenerowane API.
11. **mcp.json:** tylko GitHub. **Rozjazd:** `context.mdc` każe schemat przez MCP Postgres — serwera nie ma w mcp.json.
12. **CI:** `gate.yml` (PG 16 + OpenFGA w jobie), `codeql.yml` (upload GHAS leftover), `pr-nudge.yml` (checklist, nie egzekucja).
13. **Lokalny push:** `scripts/githooks` → `just gate` ~70 s. `agentlint` = hash kontraktu (6 czerwonych pushy na podpis, nie na kod).
14. **Knowledge:** `docs/_knowledge/` — 5 kart tools + 1 anti-poisoning; `rules-catalog` i `skills-catalog` **puste**. Retrieve max 8–20.

### 3.3 Taśma dnia vs `/noc`

| Krok | Dzień | Noc |
|---|---|---|
| Q | CURRENT | CURRENT; ignoruj pamięć czatu |
| Plan | tryb Plan, `akceptuję` | w Agencie, sam push delty |
| Plaster | nowa rozmowa, stop po planie plików | bez stopu |
| Testy | czekaj na `implementuj` | od razu kod |
| Jakość | `/po-plastrze` pełna tabela | ta sama kartka — nie pomijać |
| WIP | 1, czysty git | 1; drugi agent zakazany |

`/noc`: `scripts/noc-preflight.ps1` + plik bicia serca gitignore + skill `/loop` 15 min. To automatyzacja **lokalnej sesji**, nie Cursor Automation.

### 3.4 Automatyzacje istniejące (deterministyczne)

Hooks, git hook gate, CI, PR nudge, `/loop` w nocy, `just docs`, agentlint. **Zero** workflow na cursor.com Automations.

### 3.5 Czego nie zaplanowaliśmy (luki fabryki, nie anty-cele)

| Luka | Bezpieczny kierunek | Zakaz |
|---|---|---|
| Cursor Automations = 0 | Cron: retro checklist, komentarz przy fail CI; **zero merge** | Agent merge na `main` |
| Knowledge ~6 kart | Człowiek dodaje kartę ≤80 linii po retro | Dump 1000 repo |
| Brak ewaluacji promptów w taśmie | promptfoo na syntetykach (`synth://`) | Żywy OpenAI w gate, PDF klienta w git |
| MCP Postgres zadeklarowany, niepodłączony | Dopiąć albo poprawić `context.mdc` | Czytanie wszystkich modeli na zapas |
| Bugbot / security-review poza kolejką | Read-only na PR | Zdejmowanie HITL |
| Goals / Autopilot / Origin | Opcjonalnie po IdP; nie drugi plan | Drugi SoT obok PLAN-REALIZACJA |
| split-to-prs vs WIP=1 na main | Zostaw aż branch protection UI | Force-push, równoległe plastry |
| Gate: meta przed kodem | Leftover: kolejność jobów | Wyłączyć agentlint |
| Piątek retro ręczny ≤30 min | Automation = przypomnienie + issue | Auto-edit GROUNDING/AGENTS |
| Memories Cursor | Zakaz na cennikach (karta 001) | RAG na logikę wyceny (HC) |

### 3.6 Uczenie się — dozwolone vs zakazane

Nauka (ADR-0001): Auto-AGENTS szkodzi. Human-curated lekko pomaga. Cai 2026: ewolucja reguł. Treude: context rot.

**Wolno (propozycja, nie ma w PLAN):**

- Sygnał CI / jscpd / leftover → karta-propozycja albo issue `retro-YYYY-MM-DD` → **człowiek merge**.
- Golden exemplar po BC 4,4 (ADR #2) — agent kopiuje wzorzec, nie 30 person.
- Nested AGENTS uzupełniać przy nowym serwisie (ADR #1) — już częściowo.
- Cron piątek: checklist prune alwaysApply / skills &gt;4 tyg. — **nie** rewrite kontraktu.
- Threat-model dopisek po incydencie (63.0 już jest).

**Nie wolno:**

- LLM generuje cały AGENTS/rules.
- 30 subagentów-person.
- Memories na pipeline stawek.
- Zastąpić hooks „prośbą w prompcie”.
- Infisical, 70 stubów, RAG na SQL wyceny.

---

## 4. Stack technologiczny (przypomnienie dla Claude)

**Runtime dziś:** PostgreSQL 16 + RLS + pg_trgm · FastAPI + granian · SQLAlchemy 2 · Alembic · Pydantic v2 · OpenFGA · React 19 + Vite + TanStack + shadcn + Tailwind v4 + PostHog.

**Cel, nie runtime:** Temporal, Hatchet, OpenTelemetry (S59), pgvector, Redis, MinIO, EmailEngine.

**Auth dziś:** email+hasło+JWT ≠ IdP. Auth0 = S53.

**Jakość:** ruff, mypy strict, import-linter, jscpd próg 3%, vulture, pytest unit+integration, Playwright w CI, size-limit JS. `just perf` k6 = echo (nie DoD). Coverage 80% w AGENTS jako cel, egzekucja wg PLAN § Gate dziś vs cel.

---

## 5. Pliki, które Claude MUSI czytać

Kanon: `docs/PLAN-REALIZACJA.md`, `docs/state/CURRENT.md`, `GROUNDING.md`, `AGENTS.md`, `docs/adr/0001-cursor-software-factory-weryfikacja.md`, `docs/adr/0002-frontend-platform-2026.md`, `docs/adr/0003-frontend-ui-system-2026.md`, `docs/ops/post-plaster.md`, `docs/ops/docs-debt.md`, `docs/ops/nocna-zmiana.md`, `docs/ops/friday-retrospective.md`, `docs/ops/weekly-refactor.md`, `docs/ops/threat-model-tenant-hitl.md`, `.cursor/hooks.json`, `.cursor/settings.json`, `.cursor/mcp.json`, `.cursor/commands/*`, `.github/workflows/*`.

Jedna spec na sesję — ta z CURRENT. Nie dump `Informacje z claude/`. Jeśli potrzebny jeden M-xx z archiwum: nagłówek i obiekty tego ID, nie aneksy.

---

## 6. Prompt dla Claude (wklej jako zadanie)

Poniższy blok to instrukcja wykonawcza. Nie zmieniaj HC. Nie startuj S1 w tym zadaniu, chyba że CURRENT i operator powiedzą inaczej.

```
Jesteś architektem software house dla OmniRoute (modularny monolit spedycyjny, 1 operator + agenty Cursor).

Wejście (obowiązkowe):
- ten briefing
- docs/PLAN-REALIZACJA.md
- docs/state/CURRENT.md
- GROUNDING.md
- AGENTS.md
- docs/adr/0001-cursor-software-factory-weryfikacja.md
- docs/ops/docs-debt.md
- .cursor/ (commands, hooks, settings, mcp, skills, rules)
- canvasy jeśli operator je wklei: zakres-po-planie, software-house-cursor, moduly-wydmuszki-audyt

Cel operatora:
1. Software house ma działać jak dojrzały, prawdziwy SH: taśma, bramki, artefakty, review, dług nazwany, zero teatru.
2. Agenci i Cursor mają się uczyć, rozwijać i poprawiać — ALE automatycznie tylko tam, gdzie to bezpieczne (propozycja + człowiek merge). Nigdy auto-rewrite AGENTS.md / GROUNDING.md / HC.
3. Masz przeanalizować, poprawić, ulepszyć, zabezpieczyć, rozszerzyć i zaprojektować bezpieczną automatyzację fabryki — nie produktu spedycyjnego w tym zadaniu, chyba że zmiana fabryki wymaga jednego pliku kontraktu.

Twarde zakazy (HC i ADR-0001):
- LLM nie liczy kwot/marż/VAT/kursów. charge = prawda o marży. HITL przed zapisem stawki.
- Zero zapisu AI do bazy produkcyjnej. ExtractionService nie importuje rates.
- Nie 70 stubów. Nie Infisical. Nie Temporal/Hatchet na zapas. Nie pgvector „bo stos”. Nie Next jako app.
- Nie 30 person agentów. Nie dump Informacje z claude/. Nie RAG na wycenę/schemat DB.
- Nie Auto-AGENTS (badania: gorszy success, drożej). Nie Memories Cursor na cennikach.
- Nie git push --force na main. Nie --no-verify jako nawyk. Nie zdejmować HITL.
- Nie scoring natural_person/JDG. Nie auto-send / auto-booking / auto-przelew.
- WIP=1. Kolejka tylko z CURRENT + PLAN. Nie F9.1 bez żywej nazwy. Nie drugi SoT planu.

Dojrzały SH — definicja dla tego repo:
- Komunikacja przez artefakty (delta-spec, ADR, test report, leftover), nie chat agent↔agent.
- Deterministyczna pętla: Plan → czerwone testy → kod → post-plaster (pełna tabela) → gate → push.
- Kuracja kontekstu: ≤3 alwaysApply, skills on-demand, knowledge 8–20 kart, piątkowe prune.
- Uczenie = zbieranie sygnałów (CI, jscpd, powtórzony błąd) do kart/issue; człowiek akceptuje zmianę kontraktu.
- Automatyzacja chmurowa (Cursor Automations) wolna wyłącznie: cron przypomnień, komentarz PR, draft leftover. Zakaz: merge, edycja HC, accept extract, wysyłka maila, booking.

Dostarcz (w tej kolejności, zero kodu produktu OmniRoute w pierwszym przebiegu):

A. Werdykt 1 strona: co w fabryce zostawić, co spiąć, co świadomie nie robić.
B. Luki fabryki vs dojrzały SH — tabela: luka / ryzyko / bezpieczna zmiana / zakaz.
C. Plan uczenia (human-curated):
   - jakie karty docs/_knowledge/ dodać (≤80 linii, kategorie tools|prompts|memory-patterns) — max 15 propozycji, nie dump.
   - golden exemplars: które BC już są wzorcem (tenancy, charge, geography, extraction HITL).
   - retro: jak spiąć friday-retrospective.md z automacją-przypomnieniem bez edycji AGENTS.
D. Bezpieczne automatyzacje Cursor (szkice, nie YAML proto): nazwa, trigger, co wolno agentowi, czego nie, HITL.
   Kandydaci: (1) piątek prune checklist, (2) czerwony gate.yml → komentarz + linia docs-debt draft, (3) jscpd/refactor_ratio weekly issue, (4) po merge plastera przypomnienie post-plaster jeśli brak kartki. Żadna nie commituje sama.
E. Naprawa rozjazdów kontraktu (małe, jawne):
   - context.mdc vs brak Postgres w .cursor/mcp.json
   - leftover kolejność gate (meta przed kodem) — propozycja justfile/gate.yml, nie implementuj bez zgody
   - agentlint: jak nie powtórzyć serii #79–#88
F. Rozszerzenie mocnego zakresu produktu TYLKO jako backlog wierszy do PLAN (nie kod): how-to, Watchtower, set-based batch, KSeF, GUS gdy klucz — zgodne z Fala S, bez nowej kolejki równoległej.
G. Lista „nie ruszamy”: HC, charge/rate_line, HITL, CURRENT jako SoT sesji, zakaz person, zakaz dump archiwum.

Format: markdown w docs/ops/ albo docs/deltas/open/ jeśli to ma wejść w kolejkę jako osobny plaster fabryki. Najpierw plan plików i czekaj na akceptację operatora. Powyżej 3 plików produktu = stop. Tu wolno: 1 briefing korekta + 1 delta fabryki + ewentualnie 1 karta knowledge — po zgodzie.

Na końcu: 10 punktowa checklista „Claude nie zrobił szkody”.
```

### Uzupełnienie prompta — mockup HTML (dopisz POD blokiem powyżej; nie zastępuj go i nie zmieniaj punktów A–G)

```
Uzupełnienie (nie zmienia poprzedniego zadania):

Operator załącza działający plik HTML: omniroute-briefing-mockup.html
(ścieżka w repo: docs/design/omniroute-briefing-mockup.html).

To jest mockup briefingu, nie kod produktu i nie plaster UI.
Nie kopiuj go do frontend/. Nie traktuj go jako zakresu S1/S2 ani jako Watchtower S32.

Wzorzec stylistyczny całego produktu: docs/design/omniroute-ui.html
(hue 165, s1–s6, radius 12px/8px, IBM Plex Sans/Mono/Condensed, rail --ink).
Tokeny w frontend/src/index.css kopiują ten plik. Nie hue 106 z briefing-mockup,
nie hue 250 z app-preview. Nie kopiuj HTML do frontend/.

Dlaczego mockup jest niedokończony (świadomie):
- żywe Zlecenia to tablica-odczyt (~lista linków), nie tabela shipment (S28);
- żywe Wyceny to najgęstszy ekran, ale nadal nakładki Fali 3 bez PDF/won-lost;
- Watchtower i mapa to wizja (ui-06 / S32), mapa poza initial JS;
- tablice-odczyty nie idą na notę 5,0; HTML nie sumuje kwot w JS (HC-02);
- przycisk Akceptuj w HITL jest wyłączony — optimistic accept zakazany;
- ⌘K wyłączone, bo żyje w AppShell, nie w tym pliku.

Użyj mockupu wyłącznie jako: (1) DNA wizualne frontendu do recenzji spójności,
(2) ilustracja luki tablica vs wieża, (3) ostrzeżenie żeby nie dorysowywać
KSeF/IMAP/portali jako „już jest”. Nie rozszerzaj punktu F o nowy frontend
z tego HTML. Nie zmieniaj A–G.
```

### Uzupełnienie prompta — Cursor Multitask (dopisz POD dwoma blokami powyżej; nie zastępuj ich i nie zmieniaj A–G)

```
Uzupełnienie (nie zmienia poprzedniego zadania ani uzupełnienia o mockup):

Software house ma móc używać Cursor Multitask (okno Agentów: kilka sesji
równolegle; Cloud Agent na własnym worktree/gałęzi; subagenty w jednej
sesji; tryb Multitask obok Agent/Plan). Cel: większa przepustowość bez
kolizji w git, bez awarii CURRENT/PLAN, bez dwóch zapisów w tym samym
drzewie roboczym.

To NIE znosi WIP=1 z pierwszego bloku. Multitask nie oznacza dwóch
plastrów produktu na origin/main w tym samym czasie.

Kontrakt antykolizyjny (Claude ma to wpisać w playbook, nie w kod):

1. Jeden PISARZ produktu na jedną kopię roboczą.
   - Sesja z /plaster, /noc, commit/push trzyma wyłączność na checkout.
   - Druga sesja na TYM SAMYM drzewie = tylko Ask / Plan / odczyt.
   - /noc: zero drugiego agenta piszącego (docs/ops/nocna-zmiana.md).

2. Izolacja albo nic.
   - Równoległy zapis tylko na osobnym git worktree + osobnej gałęzi
     (Cloud Agent / best-of-n / worktree). Merge na main wyłącznie po
     człowieku + just gate. Zakaz force-push. Zakaz --no-verify.
   - Dwa agenty edytujące te same pliki (CURRENT.md, docs/deltas/open/*,
     alembic/versions/*, agentlint.baseline.json, AGENTS.md) = kolizja
     planu powstania aplikacji. Zabraniać nawet na worktree, jeśli cel
     to ten sam numer plastra / to samo Q.

3. Kolejka pozostaje jedna.
   - CURRENT.md + PLAN-REALIZACJA.md § Kolejka = jedyny SoT „co dalej”.
   - Multitask nie startuje S3, gdy CURRENT = S2. Nie równoległa Fala.
   - Drugi agent może: review PR, leftover docs-debt (propozycja), karta
     knowledge, how-to operatora, threat-model dopisek, Ask o spec —
     byle nie zmieniał numeru Q ani nie otwierał drugiej delty na to
     samo Q.

4. Subagenty wewnątrz JEDNEGO plastra — dozwolone.
   - lowca-duplikatow, explore, Bugbot/security-review read-only.
   - Zakaz 30 person. Zakaz chat agent↔agent bez artefaktu.
   - Subagent nie pushuje i nie edytuje CURRENT.

5. Cloud / worktree — pasy bezpieczne vs zakazane.
   Bezpieczne: recenzja diffu, konkurencyjne PLAN (delta w innym pliku,
   nie w docs/deltas/open/<ten-sam-id>), eksperyment UI na gałęzi
   throwaway, ewaluacja promptu extract na syntetykach.
   Zakazane: drugi /plaster tego samego M-xx; równoległa migracja
   Alembic; równoległy /zamknij; dwa /noc; merge bez rebase na świeży
   main; edycja HC/GROUNDING.

6. Awaria — definicja i hamulec.
   Awaria = dwa HEAD-y na main, rozjechany CURRENT vs git, dwie delty
   open na to samo Q, agentlint hash w jednym commicie a treść w drugim,
   /noc + Multitask piszący.
   Hamulec: preflight (czysty git, main, jeden busy w NOC-LIVE),
   worktree nie-main, człowiek scala.

Dostawa DODATKOWA (punkt H — nowy, nie edytuj A–G):
H. Playbook Multitask dla OmniRoute, 1–2 strony: tabela „tryb Cursor ×
   wolno/zakaz”; 3 pasy (pisarz plastra | czytelnik/review | worktree
   izolowany); checklista przed odpaleniem drugiej sesji; jak to spiąć
   z /noc i WIP=1 bez drugiej kolejki planu. Zero kodu produktu.
   Nie proponuj równoległych plastrów S1 i S2. Nie zmieniaj A–G.
```

---

## 7. Checklista operatora przed oddaniem Claude

- [ ] Wklej ten plik + PLAN + CURRENT + GROUNDING + AGENTS + ADR-0001.
- [ ] Dołącz trzy canvasy albo zrzuty zakładek Werdykt.
- [ ] Dołącz `docs/design/omniroute-briefing-mockup.html` jako załącznik (otwórz go sam w przeglądarce przed wysłaniem).
- [ ] Wklej **trzy** bloki: prompt z §6, uzupełnienie o mockup, uzupełnienie o Multitask. Nie edytuj pierwszego bloku.
- [ ] Powiedz wprost: **najpierw plan, zero kodu produktu, zero merge.**
- [ ] Po odpowiedzi Claude: ty akceptujesz delty fabryki; agent Cursor implementuje w WIP=1.
- [ ] Nie otwieraj `Informacje z claude/` hurtowo w tej sesji Claude.

---

## 8. Mockup HTML (załącznik)

**Plik:** `docs/design/omniroute-briefing-mockup.html`  
Kopia do załączenia z dysku: `C:\Users\sebas\.cursor\projects\d-OMNIROUTE\omniroute-briefing-mockup.html`

**Co to jest:** jeden działający plik (otwórz w Chrome/Edge). Nav przełącza widoki; przycisk Motyw przełącza `.dark`. Zero bundlera. Zero `sum()` na kwotach.

**Wzorzec:** strony **Wyceny** i **Zlecenia** z żywego `frontend/` — nie makieta sprzedażowa `omniroute-ui.html`.

**Stan niedokończony:** zamierzony. Pokazuje DNA UI + lukę (lista zleceń vs duch S28, puste miejsce mapy, HITL bez accept). Szczegóły w samym HTML (widok „Dlaczego niedokończony”) i w uzupełnieniu prompta powyżej.

---

## 9. Cursor Multitask (uzupełnienie, nie zmiana WIP=1)

PLAN już wymienia tryby Agent / Plan / Multitask jako UI Cursora. Fabryka jednak trzyma **WIP=1** na plasterze produktu i **zakaz drugiego pisarza** przy `/noc`.

Multitask wolno: druga sesja Ask/Plan na tym samym checkout; Cloud Agent / git worktree na **innej** gałęzi (review, karta knowledge, konkurencyjny plan w innym pliku); subagent read-only wewnątrz jednego plastra.

Multitask nie wolno: dwa `/plaster` albo dwa `/noc`; dwa zapisy `CURRENT.md` / tej samej delty / tej samej migracji; równoległa Fala S.

Pełny kontrakt dla Claude: uzupełnienie prompta w §6 (trzeci blok). Nie zmienia A–G.

---

## 10. Korekta po audycie Claude (2026-09-02)

Wynik audytu: [docs/deltas/open/OS-1-fabryka-uczenie-i-automacje.md](../deltas/open/OS-1-fabryka-uczenie-i-automacje.md) (A–G) i [docs/ops/multitask-playbook.md](multitask-playbook.md) (H).

**Śledzenie:** `OS-1` **nie ma wiersza w PLAN-REALIZACJA.md** — jedna linia w [docs-debt.md](docs-debt.md). Powód: fabryka nie jest osią produktu i nie może udawać wiersza Q/S.  
**Okno wykonania:** piątkowa retrospektywa. `OS-1` **nie startuje zamiast 66.0 S3**. Ten dopisek nie zmienia `CURRENT.md`.

### 10.1 Co audyt potwierdził

Werdykt §3.1 briefingu trzyma się w całości: taśma dojrzała, uczenie niezaplanowane jako pętla, Cursor Automations = 0. Liczby z canvasów (18/1/8/27/16; 12/28/14/16; taśma 7 · uczenie 2 · automacje 1) zgodne z opisem. Lista „nie wolno” z §3.6 pozostaje bez zmian.

### 10.2 Co audyt skorygował

| Punkt briefingu | Korekta |
|---|---|
| §3.2.11 — rozjazd MCP Postgres opisany jako dotyczący `context.mdc` | Rozjazd jest **także w `AGENTS.md`** § Nawigacja. Naprawa E1 rusza **dwa** pliki kontraktu, nie jeden. Ścieżka w kontrakcie: `backend/alembic/versions/` |
| §3.5 — „MCP Postgres zadeklarowany, niepodłączony → dopiąć albo poprawić” | Rozstrzygnięte: **poprawiamy kontrakt, nie dopinamy serwera.** Dopięcie = nowa powierzchnia dostępu agenta do bazy, sprzeczne z ADR-0001 #4 |
| §3.5 — „Gate: meta przed kodem” jako otwarta luka | W CI **już naprawione** (dwa niezależne joby `gate` i `meta`, PLAN § Gate). Leftover dotyczy wyłącznie **lokalnego** `just gate` przez `pre-push` (fail-fast; nazwy `code-gate` / `meta-gate` już są w `justfile`) |
| §3.3 — tabela dzień vs noc | Dopisek: `/noc` implementuje od razu po czerwonym teście, więc kartka `/po-plastrze` jest tam **najbardziej** potrzebna, nie najmniej. To najsłabsze ogniwo HITL w taśmie |
| §2.6 — pomysły na zapełnianie | Bez zmian, ale wpięte jako **propozycje wierszy do istniejących sekcji PLAN**, nigdy jako nowa oś (OS-1 §F) |

### 10.3 Wejście, którego audyt nie miał

`docs/ops/docs-debt.md`, `post-plaster.md`, `nocna-zmiana.md`, `friday-retrospective.md`, `weekly-refactor.md`, `threat-model-tenant-hitl.md`, `.cursor/commands/*`, `.cursor/rules/*`, `.cursor/skills/*`, `.github/workflows/*`, ADR-0002.

Przy umieszczeniu w repo (2026-09-02) potwierdzono: `context.mdc` zawiera zdanie o MCP; `.cursorignore` nie pokrywa `docs/_source/`; `/plaster` i skill `nowy-plaster` nadal mówią o MCP (poza E1). Twierdzenia oparte na `mcp.json`, `settings.json`, `hooks.json`, `AGENTS.md`, `GROUNDING.md`, `PLAN-REALIZACJA.md` są twarde.

### 10.4 Mockup — status po audycie

`docs/design/omniroute-briefing-mockup.html` jest spójny z ADR-0003 tam, gdzie ADR jest jeszcze leftoverem (OKLCH, oś integer/fraction/ISO, `Akceptuj` wyłączony, brak `sum()` w JS). Mockup **wyprzedza kod**. To nie jest dowód, że `U-oklch-dark` czy `U-money-align` są zrobione, i nie generuje żadnego wiersza produktu.
