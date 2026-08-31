# Dług docs/OS — świadomie poza sync 2026-08-31

Nie implementować w syncu docs. Źródło: audyt Gate/DoD + canvas `post-audit-review` + adversarial OS vs kod.

Canvas = przegląd, nie backlog do kodu na tamtą turę. Kolejność pracy: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Rejestr leftoverów.

**Zrobione w syncu (nie wracać):** nagłówek PLAN nie mówi „0.5 lokalnie”; `just test` pada przy failu unita (bez `|| true`).

- **0.10 DONE:** langfuse trace (no-op bez kluczy) + promptfoo CI na fixture’ach echo — nie cloud, nie żywy LLM
- **Następny (kod):** vitest kolejki HITL; test HTTP XOR `input_text` XOR `document_base64` (`api/extractions.py` ~45% pokrycia)
- **0.10+ produkt:** żywy instructor/OpenAI w CI, transformers llm-guard, presidio, promptfoo 30 cenników, langfuse cloud
- **Wizja, nie kod:** outbox, Temporal/Hatchet/OTel jako działające systemy
- **Backlog produktu:** JWT zamiast spoofowalnych headerów; split-screen HITL
- **Ops:** branch protection UI (GitHub Free private 403) — [branch-protection.md](branch-protection.md); `just perf` / size-limit / k6 / vulture / pip-audit = echo
- **Kontrakt FE:** nie edytuj ręcznie `frontend/src/api/*` (flatten anyOf|null → cast w wrapperze)
- **Zakaz:** fałszywe ruchy `refactor_ratio`, folder `.cursor/agents/` z personami, dump `Informacje z claude/` do nowych docs
