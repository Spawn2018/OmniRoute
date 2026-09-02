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
| 2026-09-01 | Plan 4.0 | M-05 | delta `docs/deltas/open/4.0-port.md` + spec `geography.md`. Następny: `/plaster` 4.0 w nowej rozmowie. Nie 4.1. Nie Q2. |
| 2026-09-01 | 4.0 | M-05 | `port` UN/LOCODE + RLS FORCE + `resolve` (Gdingen→PLGDY) + `/ports` + `seed_ports.py`; 45 testów integracyjnych zielonych lokalnie na PG 16; nie `location`, nie `terminal`, nie WPI |
| 2026-09-01 | ops | toolchain | `just` 1.58 w `tools/just`, PG 16 przenośny w `tools/pg16`, `lint-imports`/`psql` w PATH, `sh` z `D:\Git\bin`. **`just gate` i `just test` przechodzą lokalnie w całości** — koniec wpisów „PG wisiał, zostaje CI” |
| 2026-09-01 | kontrakt | os | wrócił próg **plan przed kodem powyżej trzech plików**, jawnie także poza kolejką Q (hotfix, leftover); w `AGENTS.md`, `context.mdc`, `/plaster`, skillu `nowy-plaster`; baseline `agentlint` przepisany |
| 2026-09-01 | 4.1 | M-05 | `location` (`unlocode`/`postal_zone`/`address`) + `location_zone_member` z typem `postal_range` (kolacja "C"), kolumną generowaną `postal_span` i exclusion GiST; `resolve(country, postal)` w Postgresie z filtrem długości; FK złożone tenant-safe do `port` (migracja dokłada brakujące `uq_port_org_id`); RLS FORCE + izolacja na obu tabelach; `/locations` z panelem zakresów; nie `terminal`, nie WPI, nie `pg_trgm` |
| 2026-09-01 | 4.2 | M-05 | `terminal` (ISPS, `operator_name` tekst, RLS FORCE, unikat częściowy, FK złożone do `port`) + kolumny WPI na `port`; ingest poza HTTP (`seed_wpi.py` + fixture); `/terminals` + kolumny WPI na `/ports`; OpenFGA bez zmian; nie `operator_party_id`, nie `kind=terminal` na `location`, nie live NGA |
| 2026-09-01 | Plan 5.0 | M-10 | delta `docs/deltas/archived/5.0-party.md` + spec `parties.md`. Cały katalog M-10 w jednym plastrze. Następny: `/plaster` 5.0 w nowej rozmowie. Nie Q3. |
| 2026-09-01 | 5.0 | M-10 | `party` + kontakty/rachunki/domeny/override/`carrier_profile`; RLS FORCE; `resolve(tax_id)`; lookup GUS/VIES/IBAN jako szkic (fixture); OpenFGA `can_manage_parties`; `/parties`; leftover `terminal.operator_party_id`. Nie Q3, nie silnik wyceny z override. |
| 2026-09-01 | Plan 5.1 | M-21 | delta `docs/deltas/open/5.1-quotation-port-party.md`: POL/POD + `party_id` na `quotation`; SQL nadal z istniejącego `rate_line`; nie override, nie k6. Następny: `/plaster` 5.1. |
| 2026-09-01 | 5.1 | M-21 | `quotation.origin_port_id` / `destination_port_id` / `party_id`; FK złożone; CHECK kompletności; lista filtruje w SQL; UI `/quotations` z pickerami. Kwota nadal ze stawki. Nie override, nie k6. |
| 2026-09-01 | Plan 5.2 | M-09 | delta `docs/deltas/archived/5.2-commodity-code.md` + spec. Katalog HS/CN per tenant. Nie podpięcie do wyceny. Następny: `/plaster` 5.2. |
| 2026-09-01 | 5.2 | M-09 | `commodity_code` HS/CN + aliasy + `source_ref` + RLS FORCE + `resolve` + OpenFGA `can_manage_commodity_codes` + `/commodity-codes`. Nie podpięcie do wyceny, nie IMDG, nie TARIC live. |
| 2026-09-01 | Plan 6.0 | M-23 | delta `docs/deltas/archived/6.0-nbp-rate.md` + spec. Katalog kursu NBP tabeli A. Nie przeliczenie wyceny. Nie M-07 `rate_line`. Następny: `/plaster` 6.0. |
| 2026-09-01 | 6.0 | M-23 | `nbp_rate` tabela A + `source_ref` + RLS FORCE + `resolve(currency, on_date)` + OpenFGA `can_manage_nbp_rates` + `/nbp-rates`. Nie przeliczenie wyceny, nie live NBP, nie M-07 `rate_line`. |
| 2026-09-01 | Plan 7.0 | M-52 | delta `docs/deltas/archived/7.0-dangerous-good.md` + spec. Katalog UN/IMDG per tenant. Nie podpięcie do wyceny. Nie M-08 `charge`. Następny: `/plaster` 7.0. |
| 2026-09-01 | 7.0 | M-52 | `dangerous_good` UN/IMDG + aliasy + `source_ref` + RLS FORCE + `resolve` + OpenFGA `can_manage_dangerous_goods` + `/dangerous-goods`. Nie podpięcie do wyceny, nie M-08 `charge`, nie live IMO. |
| 2026-09-01 | Plan 8.0 | M-11 | delta `docs/deltas/archived/8.0-party-email-match.md`. Matcher `resolve_email` na `party_email_domain`. Nie nowa tabela, nie IMAP, nie auto-INSERT kontaktu. Następny: `/plaster` 8.0. |
| 2026-09-01 | 8.0 | M-11 | `resolve_email` na `party_email_domain`; `UnknownEmailDomain`; GET `/parties/resolve-email`; pole „Sprawdź mail” na `/parties`. Nie nowa tabela, nie IMAP, nie auto-INSERT kontaktu. |
| 2026-09-01 | Plan 9.0 | M-12 | delta `docs/deltas/archived/9.0-network.md` + spec. Katalog `network` per tenant. Nie `network_member`, nie scraping, nie RapidFuzz. Następny: `/plaster` 9.0. |
| 2026-09-02 | 9.0 | M-12 | `network` katalog + `source_ref` + RLS FORCE + `resolve` + OpenFGA `can_manage_networks` + `/networks`. Nie katalog agentów, nie scraping. |
| 2026-09-02 | Plan 10.0 | M-13 | delta `docs/deltas/archived/10.0-party-scorecard.md` + spec. Snapshot `party_scorecard` per party. Nie SQL-refresh, nie scoring osoby, nie RFQ. Następny: `/plaster` 10.0. |
| 2026-09-02 | 10.0 | M-13 | `party_scorecard` snapshot + RLS FORCE + ranking + OpenFGA `can_manage_parties` + `/party-scorecards` + panel na `/parties`. Nie SQL-refresh, nie scoring osoby, nie RFQ. |
| 2026-09-02 | Plan 11.0 | M-16 | delta `docs/deltas/archived/11.0-customer-sop.md` + spec. Katalog `customer_sop` + zatwierdzenie. Nie generator zadań, nie M-35. Następny: `/plaster` 11.0. |
| 2026-09-02 | 11.0 | M-16 | `customer_sop` katalog + RLS FORCE + `resolve(party_id, code)` + zatwierdzenie + OpenFGA `can_manage_parties` + `/customer-sops` + panel na `/parties`. Nie generator zadań, nie M-35, nie `superseded_by`. |
| 2026-09-02 | Plan 12.0 | M-18 | delta `docs/deltas/archived/12.0-port-surcharge.md` + spec. Katalog `port_surcharge` per port. Nie zapis do `charge`, nie ewaluacja warunku. Następny: `/plaster` 12.0. |
| 2026-09-02 | 12.0 | M-18 | `port_surcharge` katalog extra + RLS FORCE + `resolve(port_id, code)` + OpenFGA `can_manage_geography` + `/port-surcharges` + panel na `/ports`. Nie zapis do `charge`, nie ewaluacja warunku, nie M-19 live. |
| 2026-09-02 | Plan 13.0 | M-19 | delta `docs/deltas/archived/13.0-channel-quote.md` + spec. Katalog `channel_quote` per armator+POL/POD. Nie live HTTP, nie zapis do `rate_line`. Następny: `/plaster` 13.0. |
| 2026-09-02 | 13.0 | M-19 | `channel_quote` katalog oferty + RLS FORCE + `resolve` as-of + OpenFGA `can_manage_rate_lines` + `/channel-quotes`. Nie live HTTP, nie zapis do `rate_line`/`charge`, nie IMAP. |
| 2026-09-02 | Plan 14.0 | M-14 | delta `docs/deltas/archived/14.0-credit-review.md` + spec. Katalog `credit_review` per party. Nie auto-scoring, nie zmiana `credit_limit`. Następny: `/plaster` 14.0. |
| 2026-09-02 | 14.0 | M-14 | `credit_review` katalog recenzji + RLS FORCE + `resolve` as-of + OpenFGA `can_manage_parties` + `/credit-reviews` + panel na `/parties`. Nie auto-scoring, nie zapis `credit_limit`, nie biuro HTTP. |
| 2026-09-02 | Plan 15.0 | M-15 | delta `docs/deltas/archived/15.0-finance-board.md` + spec. Tablica odczytu `/finance`. Nie nowa tabela, LLM nie liczy. Następny: `/plaster` 15.0. |
| 2026-09-02 | 15.0 | M-15 | `finance_board` tablica odczytu `/finance` (marża z `charge`, NBP, limit, recenzja). Nie nowa tabela, LLM nie liczy, nie zapis `charge`/`credit_limit`. |
| 2026-09-02 | Plan 16.0 | M-23 | delta `docs/deltas/archived/16.0-quotation-nbp.md` + spec. Wycena czyta `nbp_rate`. Nie drugi katalog, nie mnożenie kwoty. Następny: `/plaster` 16.0. |
| 2026-09-02 | 16.0 | M-23 | `nbp_rate` odczyt przy `/quotations` (waluta oferty + dzień). Nie nowa tabela, nie mnożenie `amount`, nie drugi katalog FX. |
| 2026-09-02 | Plan 17.0 | M-24 | delta `docs/deltas/archived/17.0-offer-risk.md` + spec. Wycena czyta recenzję i kartę. Nie scoring, nie nowa tabela. Następny: `/plaster` 17.0. |
| 2026-09-02 | 17.0 | M-24 | `offer_risk` odczyt recenzji i karty przy `/quotations`. Nie nowa tabela, nie scoring, nie zapis `credit_limit`. |
| 2026-09-02 | Plan 18.0 | M-25 | delta `docs/deltas/archived/18.0-offer-negotiation.md` + spec. Wycena czyta `channel_quote`. Nie wynik won/lost, nie spread. Następny: `/plaster` 18.0. |
| 2026-09-02 | 18.0 | M-25 | `offer_negotiation` odczyt `channel_quote` przy `/quotations`. Nie nowa tabela, nie odejmowanie kwot, nie zapis wyniku. |
| 2026-09-02 | Plan 19.0 | M-26 | delta `docs/deltas/archived/19.0-offer-document.md` + spec. Podgląd faktów wyceny. Nie PDF, nie U-print. Następny: `/plaster` 19.0. |
| 2026-09-02 | 19.0 | M-26 | `offer_document` podgląd faktów `quotation` na `/quotations`. Nie PDF, nie `window.print`, nie nowa tabela. |
| 2026-09-02 | Plan 20.0 | M-27 | delta `docs/deltas/archived/20.0-quotation-batch.md` + spec. Wiele kodów na lane. Nie CSV, nie nowa tabela. Następny: `/plaster` 20.0. |
| 2026-09-02 | 20.0 | M-27 | `quotation_batch` wiele kodów na jednej lane (`POST /quotations/batch`). Nie CSV, nie nowa tabela, nie set-based SQL. |
| 2026-09-02 | Plan 21.0 | M-28 | delta `docs/deltas/archived/21.0-customer-inquiry.md` + spec. Ślad wycen per party. Nie tabela RFQ, nie IMAP. Następny: `/plaster` 21.0. |
| 2026-09-02 | 21.0 | M-28 | `customer_inquiry` ślad wycen per party na `/quotations`. Nie tabela RFQ, nie IMAP, nie suma kwot. |
| 2026-09-02 | Plan 22.0 | M-29 | delta `docs/deltas/archived/22.0-offer-acceptance.md` + spec. Pending z wycen. Nie tabela wyniku, nie HITL accept. Następny: `/plaster` 22.0. |
| 2026-09-02 | 22.0 | M-29 | `offer_acceptance` pending z wycen na `/quotations`. Nie tabela wyniku, nie HITL accept, nie IMAP. |
| 2026-09-02 | Plan 23.0 | M-30 | delta `docs/deltas/archived/23.0-carrier-inquiry.md` + spec. Ślad `channel_quote` przy lane. Nie tabela RFQ, nie live HTTP. Następny: `/plaster` 23.0. |
| 2026-09-02 | 23.0 | M-30 | `carrier_inquiry` ślad `channel_quote` przy lane na `/quotations`. Nie tabela RFQ, nie live HTTP, nie odejmowanie kwot. |
| 2026-09-02 | Plan 24.0 | M-31 | delta `docs/deltas/archived/24.0-response-comparison.md` + spec. Zestawienie kwot na POL/POD. Nie tabela, nie spread w JS. Następny: `/plaster` 24.0. |
| 2026-09-02 | 24.0 | M-31 | `response_comparison` zestawienie wyceny i `channel_quote` na POL/POD. Nie tabela, nie odejmowanie kwot, nie silnik spread. |
| 2026-09-02 | Plan 25.0 | M-32 | delta `docs/deltas/archived/25.0-mail-integration.md` + spec. Tablica znanych adresów. Nie IMAP, nie tabela skrzynki. Następny: `/plaster` 25.0. |
| 2026-09-02 | 25.0 | M-32 | `mail_integration` tablica `/mail` (domeny, kontakty, resolve_email). Nie IMAP, nie tabela skrzynki, nie sekrety. |
| 2026-09-02 | Plan 26.0 | M-33 | delta `docs/deltas/archived/26.0-mail-client.md` + spec. `mailto:` na `/mail`. Nie Office.js, nie Graph. Następny: `/plaster` 26.0. |
| 2026-09-02 | 26.0 | M-33 | `mail_client` `mailto:` z `party_contact.email` na `/mail`. Nie Office.js, nie Graph, nie IMAP. |
| 2026-09-02 | Plan 27.0 | M-34 | delta `docs/deltas/archived/27.0-operator-notice.md` + spec. Tablica HITL i wycen pending. Nie tabela, nie wysyłka. Następny: `/plaster` 27.0. |
| 2026-09-02 | 27.0 | M-34 | `operator_notice` tablica `/notifications` (HITL pending + wyceny pending). Nie tabela, nie wysyłka, nie HITL accept. |
| 2026-09-02 | Plan 28.0 | M-35 | delta `docs/deltas/archived/28.0-shipment.md` + spec. Tablica wycen z `party_id`. Nie tabela `shipment`, nie tracking. Następny: `/plaster` 28.0. |
| 2026-09-02 | 28.0 | M-35 | `shipment` tablica `/shipments` (wyceny z `party_id`). Nie tabela, nie tracking, nie odcinki. |
| 2026-09-02 | Plan 29.0 | M-36 | delta `docs/deltas/archived/29.0-tracking.md` + spec. Tablica lane POL/POD. Nie tabela zdarzeń, nie mapa. Następny: `/plaster` 29.0. |
| 2026-09-02 | 29.0 | M-36 | `tracking` tablica `/tracking` (lane POL/POD + UN/LOCODE). Nie tabela, nie AIS, nie mapa. |
| 2026-09-02 | Plan 30.0 | M-37 | delta `docs/deltas/archived/30.0-operational-exception.md` + spec. Tablica wycen z party bez pełnego POL/POD. Nie tabela zdarzeń, nie mapa. Następny: `/plaster` 30.0. |
| 2026-09-02 | 30.0 | M-37 | `operational_exception` tablica `/exceptions` (party bez pełnego POL/POD). Nie tabela, nie AIS, nie mapa. |
| 2026-09-02 | Plan 31.0 | M-38 | delta `docs/deltas/archived/31.0-shipment-document.md` + spec. Tablica `source_ref` wycen z party. Nie tabela HBL, nie PDF. Następny: `/plaster` 31.0. |
| 2026-09-02 | 31.0 | M-38 | `shipment_document` tablica `/shipment-documents` (`source_ref` wycen z party). Nie tabela, nie PDF, nie HBL. |
| 2026-09-02 | Plan 32.0 | M-39 | delta `docs/deltas/archived/32.0-edi-message.md` + spec. Tablica `channel_quote` na lane. Nie tabela EDI, nie X12. Następny: `/plaster` 32.0. |
| 2026-09-02 | 32.0 | M-39 | `edi_message` tablica `/edi` (`channel_quote` na lane wyceny). Nie tabela, nie X12, nie live HTTP. |
| 2026-09-02 | Plan 33.0 | M-40 | delta `docs/deltas/archived/33.0-sales-invoice.md` + spec. Tablica sell z charge. Nie tabela FV, nie KSeF. Następny: `/plaster` 33.0. |
| 2026-09-02 | 33.0 | M-40 | `sales_invoice` tablica `/invoices` (sell z charge). Nie tabela, nie KSeF, nie odejmowanie kwot. |
| 2026-09-02 | Plan 34.0 | M-41 | delta `docs/deltas/archived/34.0-quote-invoice-settlement.md` + spec. Tablica wycena + sell po `rate_line_id`. Nie tabela rozliczenia. Następny: `/plaster` 34.0. |
| 2026-09-02 | 34.0 | M-41 | `quote_invoice_settlement` tablica `/quote-invoices` (wycena + sell po `rate_line_id`). Nie tabela, nie odejmowanie kwot. |
| 2026-09-02 | Plan 35.0 | M-42 | delta `docs/deltas/archived/35.0-bank-payment.md` + spec. Tablica IBAN + sell. Nie tabela płatności. Następny: `/plaster` 35.0. |
| 2026-09-02 | 35.0 | M-42 | `bank_payment` tablica `/payments` (IBAN + sell z charge). Nie tabela płatności, nie SEPA, nie N+1. |
| 2026-09-02 | Plan 36.0 | M-43 | delta `docs/deltas/archived/36.0-money-cost.md` + spec. Tablica NBP + buy. Nie tabela odsetek. Następny: `/plaster` 36.0. |
| 2026-09-02 | 36.0 | M-43 | `money_cost` tablica `/money-cost` (NBP + buy z charge). Nie tabela odsetek, nie mnożenie kursem. |
| 2026-09-02 | Plan 37.0 | M-44 | delta `docs/deltas/archived/37.0-fx-difference.md` + spec. Tablica NBP walut z charge/quotation. Nie tabela FX. Następny: `/plaster` 37.0. |
| 2026-09-02 | 37.0 | M-44 | `fx_difference` tablica `/fx-differences` (NBP walut z charge/quotation). Nie tabela, nie przeliczenie. |
| 2026-09-02 | Plan 38.0 | M-45 | delta `docs/deltas/archived/38.0-cash-flow.md` + spec. Tablica buy+sell jako wypływ/wpływ. Nie tabela księgi. Następny: `/plaster` 38.0. |
| 2026-09-02 | 38.0 | M-45 | `cash_flow` tablica `/cashflows` (buy=wypływ, sell=wpływ). Nie tabela księgi, nie odejmowanie. |
| 2026-09-02 | Plan 39.0 | M-46 | delta `docs/deltas/archived/39.0-cost-to-serve.md` + spec. Tablica SOP + wyceny kontrahenta. Nie tabela ABC. Następny: `/plaster` 39.0. |
| 2026-09-02 | 39.0 | M-46 | `cost_to_serve` tablica `/cost-to-serve` (SOP + wyceny kontrahenta). Nie tabela ABC, nie suma kwot. |
| 2026-09-02 | Plan 40.0 | M-47 | delta `docs/deltas/archived/40.0-bookkeeping.md` + spec. Tablica charge + nazwa kodu. Nie JPK. Następny: `/plaster` 40.0. |
| 2026-09-02 | 40.0 | M-47 | `bookkeeping` tablica `/bookkeeping` (charge + charge_code.name). Nie JPK, nie ERP. |
| 2026-09-02 | Plan 41.0 | M-48 | delta `docs/deltas/archived/41.0-road-transport.md` + spec. Tablica location postal_zone/address. Nie TMS. Następny: `/plaster` 41.0. |
| 2026-09-02 | 41.0 | M-48 | `road_transport` tablica `/road` (postal_zone i address). Nie TMS, nie GPS. |
| 2026-09-02 | Plan 42.0 | M-49 | delta `docs/deltas/archived/42.0-intermodal-rail.md` + spec. Tablica portów z flagą rail. Nie wagon. Następny: `/plaster` 42.0. |
| 2026-09-02 | 42.0 | M-49 | `intermodal_rail` tablica `/rail` (porty z flagą rail). Nie wagon, nie CIM. |
| 2026-09-02 | Plan 43.0 | M-50 | delta `docs/deltas/archived/43.0-china-rail.md` + spec. Tablica portów CN z flagą rail. Nie korytarz. Następny: `/plaster` 43.0. |
| 2026-09-02 | 43.0 | M-50 | `china_rail` tablica `/china-rail` (porty CN z flagą rail). Nie korytarz, nie HTTP. |
| 2026-09-02 | Plan 44.0 | M-51 | delta `docs/deltas/archived/44.0-ocean-lcl.md` + spec. Tablica portów `is_seaport`. Nie tabela LCL. Następny: `/plaster` 44.0. |
| 2026-09-02 | 44.0 | M-51 | `ocean_lcl` tablica `/lcl` (porty z `is_seaport`). Nie tabela LCL, nie CFS. |
| 2026-09-02 | Plan 45.0 | M-53 | delta `docs/deltas/archived/45.0-sanctions.md` + spec. Tablica aktywnych party tax_id/country. Nie OFAC. Następny: `/plaster` 45.0. |
| 2026-09-02 | 45.0 | M-53 | `sanctions` tablica `/sanctions` (aktywni party, tax_id i kraj). Nie OFAC, nie HTTP. |
| 2026-09-02 | Plan 46.0 | M-56 | delta `docs/deltas/archived/46.0-gdpr.md` + spec. Tablica `app_user` email. Nie wnioski. Następny: `/plaster` 46.0. |
| 2026-09-02 | 46.0 | M-56 | `gdpr` tablica `/gdpr` (emaile kont tenanta). Nie wniosek, nie usuwanie. |
| 2026-09-02 | Plan 47.0 | M-57 | delta `docs/deltas/archived/47.0-ai-copilot.md` + spec. Tablica extraction pending. Nie czat. Następny: `/plaster` 47.0. |
| 2026-09-02 | 47.0 | M-57 | `ai_copilot` tablica `/ai` (szkice pending, source_ref). Nie czat, nie accept. |
| 2026-09-02 | Plan 48.0 | M-68 | delta `docs/deltas/archived/48.0-observability.md` + spec. Tablica `fetchHealth`. Nie OTel. Następny: `/plaster` 48.0. |
| 2026-09-02 | 48.0 | M-68 | `observability` tablica `/health` (`fetchHealth`). Nie OTel, nie k6. |
| 2026-09-02 | Plan 49.0 | M-69 | delta `docs/deltas/archived/49.0-extraction-quality.md` + spec. Tablica unparsed_regions. Nie scoring. Następny: `/plaster` 49.0. |
| 2026-09-02 | 49.0 | M-69 | `extraction_quality` tablica `/quality` (`unparsed_regions`). Nie scoring, nie tabela QA. |
| 2026-09-02 | Plan 50.0 | M-70 | delta `docs/deltas/archived/50.0-tenant-rollout.md` + spec. Tablica `default_currency`. Nie tabela rollout. Następny: `/plaster` 50.0. |
| 2026-09-02 | 50.0 | M-70 | `tenant_rollout` tablica `/rollout` (`default_currency`). Nie tabela, nie upsert. |
| 2026-09-02 | Plan 51.0 | U-oklch-dark | delta `docs/deltas/open/51.0-oklch-dark.md` + spec. Tokeny oklch + `.dark`. Następny: `/plaster` 51.0. |
