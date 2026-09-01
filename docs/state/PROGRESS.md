# Historia plastrów

| Data | Plaster | Moduł | Opis |
|---|---|---|---|
| 2026-08-31 | Phase 0 | — | GitHub: repo Spawn2018/OmniRoute, init, initial commit, push na origin/main |
| 2026-08-31 | Phase A | — | Bootstrap Cursor OS: AGENTS.md, GROUNDING.md, rules, skills, hooks, gate.yml |
| 2026-08-31 | ADR-0001 | — | Weryfikacja Cursor factory (Gemini/ChatGPT/nauka) → docs/adr |
| 2026-08-31 | CI fix | — | Bootstrap gate: agent-refs only do Fazy B (58facbd) |
| 2026-08-31 | Plan sync | — | Plan Cursor zsynchronizowany ze stanem repo |
| 2026-08-31 | Phase A.5 | — | gh CLI auth, .env.example, plan w .cursor/plans/ |
| 2026-08-31 | Phase B.1 | — | pyproject.toml, FastAPI, docker-compose, alembic |
| 2026-08-31 | 0.3 | M-01 | RLS Golden Standard: organization, app_user, test izolacji |
| 2026-08-31 | Phase B.3 | — | Pełny gate: ruff, mypy, pytest-unit, import-linter + CI postgres |
| 2026-08-31 | 0.4 | M-01 | OpenFGA hello: model, klient, require_permission, CI green |
| 2026-08-31 | ADR-0002 | — | Frontend platform 2026 (Thoughtworks/SoR/NN/G) + DataTableShell |
| 2026-08-31 | Audyt | — | Gate vs DoD + B.7 Free/403 wciągnięte do planu, AGENTS, skills, rules |
| 2026-08-31 | 0.5 | UI | Frontend Shell: Vite, Compiler, TanStack R/Q/Form, shadcn, ⌘K, PostHog, /tenancy/users |
| 2026-08-31 | 0.6 | UI/M-01 | DataTableShell + table_view RLS + ColumnEditor DnD + ViewManager + vitest |
| 2026-08-31 | B.7 | ops | Branch protection: procedura ręczna (Free private 403) — docs/ops/branch-protection.md |
| 2026-08-31 | Jakość | — | openapi-ts + cov≥80% + jscpd≤3% w gate + lazy PostHog |
| 2026-08-31 | 0.7 | M-20 | AI extract HITL: extraction_draft RLS, MockExtractor, OpenFGA, UI queue |
| 2026-08-31 | Faza C scaffold | AI | docling stub, langfuse no-op, promptfoo.yaml, knowledge cards |
| 2026-08-31 | Faza D | ops | agentlint w gate, pr-nudge.yml, weekly-refactor + friday-retrospective |
| 2026-08-31 | 0.8 | M-20 | instructor + llm-guard: schemat Pydantic, guard przed modelem, CI=mock |
| 2026-08-31 | 0.9 | M-20 | docling A/B: fingerprint, pdf_strings vs docling, ab_delta_chars, upload |
| 2026-08-31 | docs/OS | — | Honesty sync: PLAN/README/ARCHITECTURE/MODULES/ADR/skills/rules + spec M-20; delty 0.3/0.4 archived; `just test` bez `|| true`; leftovery audytu w PLAN + docs-debt.md |
| 2026-08-31 | 0.10 | M-20 | langfuse trace przy extract (no-op bez kluczy) + `just promptfoo` pytest echo |
| 2026-08-31 | ops | — | Pętla po każdym kroku: docs/ops/post-plaster.md (pomiar → naprawa → docs-debt) |
| 2026-08-31 | 0.11 | M-20 | HTTP XOR 422 + vitest extractionCreateBody (kolejka HITL) |
| 2026-08-31 | 0.12 | M-01 | JWT HS256 session: Bearer claims, nie spoofowalne headery |
| 2026-08-31 | 0.13 | M-20 | split-screen HITL: podgląd input_text \| recenzja kandydatów |
| 2026-08-31 | 0.14 | M-20 | HTTP happy-path extract/list/accept/reject (JWT, stub serwisu) |
| 2026-08-31 | docs/OS | — | kanon `/testy` `/bramka` zamiast person z archiwum |
| 2026-08-31 | 0.15 | M-01 | hasła argon2id + rotacja refresh; UUID-login wycięty |
| 2026-09-01 | docs/OS | FE | Exit Wave FE: twardy pasek powierzchni 2026 (U-density…U-admin-ref, Art. 50 UI); adapter+RTL nie zamyka fali |
| 2026-09-01 | D0 | OS | uczciwość OS: stos dziś vs cel; GitHub Encrypted Secrets; `.cursorignore` dump; leftover≠DONE; HITL bez zmian |
| 2026-09-01 | 0.15 T0 | M-20 | `document_base64` max_length → 422 przed decode |
| 2026-09-01 | 0.16 T1 | M-01 | rola `omniroute_app` NOBYPASSRLS; runtime URL; RLS integration = CI |
| 2026-09-01 | 0.17 T2 | M-01 | matryca RLS S1–S6 + WITH CHECK; integration = CI |
| 2026-09-01 | 0.18 | M-20 | HTTP extract live PG; token A / draft B → 404; integration = CI |
| 2026-09-01 | 0.19 A1 | API | undeclared `/api/v1` → 403; playground off |
| 2026-09-01 | 0.20 A2 | AuthZ | `can_review_extractions` = reviewer; member nie recenzuje |
| 2026-09-01 | 0.21 T4 | M-01 | `hello_token` default false; mint UUID tylko local/CI |
| 2026-09-01 | 0.22 T5 | M-01 | JWT iss/aud/jti/ver; TTL 15 min |
| 2026-09-01 | 0.23 S1 | ops | JWT_SECRET z GitHub Encrypted Secrets, nie YAML |
| 2026-09-01 | Exit Wave A | — | D0 + 0.15 T0 … 0.23 na origin. Charge/FE/Auth0 nie startowane. |
| 2026-09-01 | 0.25 | domain | Money Decimal + waluta ISO 4217 + `<Money/>` na HITL; bez tabeli charge |
| 2026-09-01 | 1.0 | M-06 | `charge_code` katalog + aliasy + RLS + `/charge-codes`; nie luźny string |
| 2026-09-01 | 1.1 | M-07 | `rate_line` immutable + `source_ref` + `/rate-lines`; nie `charge` / accept |
| 2026-09-01 | 1.2 | M-08 | `charge` buy+sell na jednym wierszu + `margin()` w kodzie + `/charges`; nie accept HITL |
| 2026-09-01 | 1.3 | M-20 | accept HITL → `rate_line` (kupno) w jednej transakcji HTTP; ExtractionService bez rates; nie outbox |
| 2026-09-01 | U-art50 | M-20 UI | label „propozycja AI” na recenzji HITL; Art. 50 = UI, nie PDF prawny |
| 2026-09-01 | U-palette-ops | UI | ⌘K: extract, accept-focus, save-view, clear-session; nie tylko nawigacja |
| 2026-09-01 | U-density | UI | compact default + toggle na users / charge-codes / rate-lines / charges / extractions |
| 2026-09-01 | U-a11y | UI | skip-to-main + `:focus-visible` + ścieżka Tab/⌘K; RTL ≠ DoD |
| 2026-09-01 | U-size-limit-real | ops/FE | `just perf` size-limit initial JS gzip < 250 kB; w gate; echo usunięte |
| 2026-09-01 | U-pdf-spans | M-20 UI | PDF viewer + highlight spanów HITL; lazy pdf.js; bez OCR |
| 2026-09-01 | U-admin-ref | UI | gęsty admin: sidebar, toolbar, ⌘K; pulpit = joby, nie hello-dashboard |
| 2026-09-01 | U-routes-breadth | UI/program | standing: Charge 1.0–1.2 mają trasy; nowe BC = UI w tym samym plasterze; nie 70 stubów |
| 2026-09-01 | docs/OS | program | Auth0 I1/I2 **odroczone** (brak tenanta). Sesja = email+hasło+JWT. |
| 2026-09-01 | 0.24 | ops | pip-audit projektu + SHA pin Actions + `/ready` + `X-Request-ID`; nie w local gate |
| 2026-09-01 | 2.1–2.2 | M-20 | Presidio stub tylko instructor + 10 syntetyk `synth://`; zero PDF klienta; nie Presidio-all |
| 2026-09-01 | 2.0 | M-21 | `quotation` INSERT…SELECT z bieżącego `rate_line` + RLS + `/quotations`; nie k6; nie marża |
| 2026-09-01 | 3.0 | M-03 | `organization_setting` allowlista `default_currency` + RLS + `/organization-settings`; nie sekrety |
| 2026-09-01 | ADR-0003 | UI | System UI: OKLCH/dark, Radix pin, wzorce HITL/charge/tenant; makiety `docs/design/`; **nie Q1**; zero kodu `frontend/` |
| 2026-09-01 | CI | ops | gate: 005 `current_database()` zamiast `Connection.url`; `docs-debt` path; URI ≠ plik w agent-refs |
| — | leftover | Auth0 | I1/I2 **odroczone** aż będzie tenant. Nie pytać. 0.12/0.15 ≠ IdP. |
| — | leftover | produkt | **Następny:** 4.0 M-05 `port` (`/plaster`). Leftovery UI ADR-0003 **nie** zamiast 4.0. M-02 parked. |
