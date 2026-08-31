# Dług techniczny — żywy rejestr

Aktualizuj **po każdym plasterze** (pętla `docs/ops/post-plaster.md`). Nie dumpuj audytu od nowa.

Źródło początkowe: audyt Gate/DoD + canvas `post-audit-review` (przegląd, nie lista do kodu).

Kolejność pracy: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Rejestr leftoverów.

**Zrobione w syncu (nie wracać):** nagłówek PLAN nie mówi „0.5 lokalnie”; `just test` pada przy failu unita (bez `|| true`).

- **0.10 DONE:** langfuse trace (no-op bez kluczy) + `just promptfoo` pytest echo — nie cloud, nie żywy LLM, nie `npx promptfoo eval`
- **0.11 DONE:** HTTP XOR 422 + vitest `extractionCreateBody`; `api/extractions.py` happy-path/accept nadal bez testu HTTP
- **0.12 DONE:** JWT HS256 hello (`Authorization: Bearer`); identity z claims; OpenFGA nadal AuthZ
- **0.13 DONE:** split-screen HITL (podgląd `input_text` | recenzja); nie PDF canvas
- **Następny (kod):** HTTP happy-path extract/accept/reject
- **Po 0.10 (eval):** `npx promptfoo eval` — lokalnie ENOSPC / playwright peers; 30 cenników = osobna decyzja danych
- **0.10+ produkt:** żywy instructor/OpenAI w CI, transformers llm-guard, presidio, promptfoo 30 cenników, langfuse cloud
- **Wizja, nie kod:** outbox, Temporal/Hatchet/OTel jako działające systemy
- **Backlog produktu:** OAuth/OIDC / hasła / refresh; HTTP happy-path extract/accept/reject
- **Ops:** branch protection UI (GitHub Free private 403) — [branch-protection.md](branch-protection.md); `just perf` / size-limit / k6 / vulture / pip-audit = echo
- **Kontrakt FE:** nie edytuj ręcznie `frontend/src/api/*` (flatten anyOf|null → cast w wrapperze)
- **Zakaz:** fałszywe ruchy `refactor_ratio`, folder `.cursor/agents/` z personami, dump `Informacje z claude/` do nowych docs
