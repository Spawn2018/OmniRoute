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
- **0.18 DONE:** HTTP extract live PG + token A / draft B → 404; integration = CI
- **0.19 A1 DONE:** undeclared `/api/v1` → 403; Swagger/ReDoc off
- **0.20 A2 DONE:** `can_review_extractions` = reviewer; seed first-login = member
- **0.21 T4 DONE:** `hello_token` default false; mint UUID tylko przy fladze
- **0.22 T5 DONE:** JWT iss/aud/jti/ver; TTL 15 min
- **0.23 S1 DONE:** JWT_SECRET z GitHub Encrypted Secrets; literał usunięty z gate.yml
- **U-routes-breadth DONE:** standing (Charge 1.0–1.2 mają trasy). **Następny (kod):** Auth0 I1. Exit Wave FE **nie** claim — nie 70 UI, nie „powierzchnia 2026”
- **U-admin-ref DONE:** pulpit = joby operatora; sidebar/toolbar/⌘K.
- **U-pdf-spans DONE:** viewer PDF + spany HITL; lazy pdf.js. Draft nie trzyma PDF (tylko input_text).
- **U-size-limit-real DONE:** `just perf` = build + gzip initial JS < 250 kB; w `just gate`. k6/vulture/pip-audit nadal echo.
- **U-a11y DONE:** skip-to-main + `:focus-visible` + ścieżka operatora.
- **U-density DONE:** compact + toggle na users / charge-codes / rate-lines / charges / extractions.
- **U-palette-ops DONE:** ⌘K akcje operatora (extract, accept-focus, save-view, clear-session).
- **U-art50 DONE:** label „propozycja AI” na recenzji HITL.
- **1.3 DONE:** accept HITL + `rate_line` (kupno) w jednej transakcji HTTP; `ExtractionService` nie importuje rates.
- **1.2 DONE:** `charge` buy+sell + `margin(buy, sell)` + `/charges`. Nie accept HITL
- **1.3 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał przy `pytest -m integration` (jak 0.16–1.2); `just api-types` nie regen — `rate_line_ids` w wrapperze nieczytane, gate = typecheck; brak MCP Postgres w sesji — nowej tabeli nie było; Wave FE U-* i Auth0 I1 nie startowane (CURRENT = I1)
- **U-routes-breadth:** 1.3 = status + link `/rate-lines` na HITL. Nie Exit Wave FE (U-density…U-admin-ref)
- **1.1 DONE:** `rate_line` immutable + `source_ref` + `/rate-lines`. Nie `charge` / marża
- **1.0 DONE:** `charge_code` katalog + aliasy + RLS + `/charge-codes`. Nie `rate_line` / `charge`
- **0.25 DONE:** Money Decimal + waluta + `<Money/>` na HITL. Bez tabeli charge
- **Exit Wave A:** D0 + T0…0.23. 0.24 pip-audit opcjonalny
- **U-routes-breadth:** 1.2 ma `/charges`. 1.1 ma `/rate-lines`. 1.0 ma `/charge-codes`. Nie Exit Wave FE (U-density…U-admin-ref)
- **1.2 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał przy `pytest -m integration` (jak 0.16–1.1); `just api-types` nie regen — wrapper fetch, gate = typecheck; brak MCP Postgres w sesji — schemat z migracji 008/009
- **1.1 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał przy `pytest -m integration` (jak 0.16–0.18 / 1.0); `just api-types` nie regen — wrapper fetch, gate = typecheck
- **1.0 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał (jak 0.16–0.18); `just api-types` nie regen — wrapper fetch, gate = typecheck
- **1.0 leftover:** aliasy jako `TEXT[]` na wierszu, nie osobna tabela — wystarcza resolve; osobny wiersz aliasu gdy 1.1+ tego wymaga
- **Leftover ≠ DONE:** wiersz w tym pliku / PLAN nie zamyka plastra i nie zastępuje `just gate`
- **OAuth/OIDC:** Auth0 I1 = następny kod (BFF+PKCE+cookie). 0.12 JWT = hello HS256, nie IdP
- **0.11 DONE:** HTTP XOR 422 + vitest `extractionCreateBody`
- **0.12 DONE:** JWT HS256 hello (`Authorization: Bearer`); identity z claims; OpenFGA nadal AuthZ
- **0.13 DONE:** split-screen HITL (podgląd `input_text` | recenzja); nie PDF canvas
- **0.14 DONE:** HTTP extract/list/accept/reject (unit + stub `ExtractionService`); `api/extractions.py` ~97%; nie live Postgres
- **0.10 DONE:** langfuse trace (no-op bez kluczy) + `just promptfoo` pytest echo — nie cloud, nie żywy LLM, nie `npx promptfoo eval`
- **Po 0.10 (eval):** `npx promptfoo eval` — lokalnie ENOSPC / playwright peers; 30 cenników = osobna decyzja danych
- **0.10+ produkt:** żywy instructor/OpenAI w CI, transformers llm-guard, presidio, promptfoo 30 cenników, langfuse cloud
- **Wizja, nie kod:** outbox, Temporal/Hatchet/OTel jako działające systemy
- **Backlog produktu:** HTTP extract vs live Postgres. PDF canvas HITL = U-pdf-spans (lazy); draft nadal bez blob PDF
- **0.14 leftover (dlaczego nie w tym plasterze):** `api/extractions.py:78` `UnparseableDocument("Brak input_text")` — gałąź obronna po XOR Pydantic (0.11); C901/jscpd na diffie czyste, bez refaktoru testów HTTP
- **Ops:** branch protection UI (GitHub Free private 403) — [branch-protection.md](branch-protection.md); k6 / vulture / pip-audit = echo; `just perf` = size-limit (U-size-limit-real)
- **Kontrakt FE:** nie edytuj ręcznie `frontend/src/api/*` (flatten anyOf|null → cast w wrapperze)
- **Zakaz:** fałszywe ruchy `refactor_ratio`, folder `.cursor/agents/` z personami, dump `Informacje z claude/` do nowych docs
