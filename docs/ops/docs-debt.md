# Dług techniczny — żywy rejestr

Aktualizuj **po każdym plasterze** (pętla `docs/ops/post-plaster.md`). Nie dumpuj audytu od nowa.

Źródło początkowe: audyt Gate/DoD + canvas `post-audit-review` (przegląd, nie lista do kodu).

Kolejność pracy: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Rejestr leftoverów.

**Zrobione w syncu (nie wracać):** nagłówek PLAN nie mówi „0.5 lokalnie”; `just test` pada przy failu unita (bez `|| true`).

- **OS słownik DONE:** kanon `/testy` / `/bramka` / skill `zamknij-plaster`; persony z archiwum tylko w tabeli ADR-0001; lint w `check_agent_refs.py`
- **0.15 DONE:** hasła argon2id + `refresh_token` + rotacja; UUID-login wycięty. RLS isolation = integration CI (lokalnie PG wisiał)
- **D0 DONE:** AGENTS stos dziś vs cel; Infisical wycięty; `.cursorignore` na dump; `AGENTS.ARCHIVE.md`; leftover ≠ DONE. HITL i 13 zasad zostają.
- **0.15 T0 DONE:** `document_base64` max_length 2_666_668 → 422 przed decode
- **0.16 T1 DONE:** rola `omniroute_app` NOBYPASSRLS; `DATABASE_URL` runtime. Integration RLS = CI (lokalnie PG wisiał)
- **0.17 T2 DONE:** WITH CHECK + matryca S1–S6; integration = CI
- **Następny (kod):** 0.18 HTTP extract live PG + cross-tenant 404 ([PROGRAM-12M.md](../state/PROGRAM-12M.md))
- **Leftover ≠ DONE:** wiersz w tym pliku / PLAN nie zamyka plastra i nie zastępuje `just gate`
- **OAuth/OIDC:** Auth0 I1 **po Wave A**; nie następny kod. 0.12 JWT = hello HS256
- **0.11 DONE:** HTTP XOR 422 + vitest `extractionCreateBody`
- **0.12 DONE:** JWT HS256 hello (`Authorization: Bearer`); identity z claims; OpenFGA nadal AuthZ
- **0.13 DONE:** split-screen HITL (podgląd `input_text` | recenzja); nie PDF canvas
- **0.14 DONE:** HTTP extract/list/accept/reject (unit + stub `ExtractionService`); `api/extractions.py` ~97%; nie live Postgres
- **0.10 DONE:** langfuse trace (no-op bez kluczy) + `just promptfoo` pytest echo — nie cloud, nie żywy LLM, nie `npx promptfoo eval`
- **Po 0.10 (eval):** `npx promptfoo eval` — lokalnie ENOSPC / playwright peers; 30 cenników = osobna decyzja danych
- **0.10+ produkt:** żywy instructor/OpenAI w CI, transformers llm-guard, presidio, promptfoo 30 cenników, langfuse cloud
- **Wizja, nie kod:** outbox, Temporal/Hatchet/OTel jako działające systemy
- **Backlog produktu:** HTTP extract vs live Postgres; PDF canvas
- **0.14 leftover (dlaczego nie w tym plasterze):** `api/extractions.py:78` `UnparseableDocument("Brak input_text")` — gałąź obronna po XOR Pydantic (0.11); C901/jscpd na diffie czyste, bez refaktoru testów HTTP
- **Ops:** branch protection UI (GitHub Free private 403) — [branch-protection.md](branch-protection.md); `just perf` / size-limit / k6 / vulture / pip-audit = echo
- **Kontrakt FE:** nie edytuj ręcznie `frontend/src/api/*` (flatten anyOf|null → cast w wrapperze)
- **Zakaz:** fałszywe ruchy `refactor_ratio`, folder `.cursor/agents/` z personami, dump `Informacje z claude/` do nowych docs
