# Historia plastrów

| Data | Plaster | Moduł | Opis |
|---|---|---|---|
| 2026-09-11 | 313.0 | CI1 | HITL `sla_clause` na customer_contract. Nie extract. Nie kara. Nastepny: pin HITL Plan. |
| 2026-09-11 | 312.0 | UI | `/refaktor`: SourceRefField na local/charge-template/cod. Label-form SourceRef DONE. Nastepny: HITL pin Plan. |
| 2026-09-11 | 311.0 | UI | `/refaktor`: SourceRefField na rate-card/fuel/groupage. Nastepny: leftover label-form. |
| 2026-09-11 | 310.0 | UI | `/refaktor`: SourceRefField na round/matrix/side. Nastepny: leftover label-form. |
| 2026-09-11 | 309.0 | UI | `/refaktor`: SourceRefField na lot/lane/quote. Nastepny: leftover label-form. |
| 2026-09-11 | 308.0 | UI | `/refaktor`: SourceRefField na prospect/win-loss/data-room. Nastepny: leftover label-form. |
| 2026-09-11 | 307.0 | UI | `/refaktor`: SourceRefField na rfp-intake/playbook/consortium. Nastepny: leftover label-form. |
| 2026-09-11 | 306.0 | UI | `/refaktor`: SourceRefField na otif/enforcement/task-template. Nastepny: leftover label-form. |
| 2026-09-11 | 305.0 | UI | `/refaktor`: SourceRefField na freight-audit/collaboration/match. Nastepny: leftover label-form. |
| 2026-09-11 | 304.0 | UI | `/refaktor`: SourceRefField na asn/routing-guide/capa. Nastepny: leftover label-form. |
| 2026-09-11 | 303.0 | UI | `/refaktor`: SourceRefField na po-line/visibility/sap. Nastepny: leftover label-form. |
| 2026-09-11 | 302.0 | UI | `/refaktor`: SourceRefField na kek/PO/terminal-slot. Nastepny: po-line/visibility. |
| 2026-09-11 | 301.0 | UI | `/refaktor`: SourceRefField na erp/idp/contract. Nastepny: connector forms. |
| 2026-09-11 | 300.0 | UI | `/refaktor`: SourceRefField na prediction/weather/exchange. Nastepny: connector forms. |
| 2026-09-11 | 299.0 | UI | `/refaktor`: SourceRefField na rank/executive/memory. Nastepny: prediction/weather. |
| 2026-09-11 | 298.0 | UI | `/refaktor`: SourceRefField na war-room/twin/tower. Nastepny: label-form. |
| 2026-09-11 | 297.0 | UI | `/refaktor`: SourceRefField na circle/lane-km/plan-snapshot. Nastepny: label-form. |
| 2026-09-11 | 296.0 | UI | `/refaktor`: HintField na TED/award-review/bid-stance. Nastepny: paper-form/label-form. |
| 2026-09-11 | 295.0 | UI | `/refaktor`: HintField na lane-pattern/monitoring/tender-carbon. Nastepny: tender paper-form. |
| 2026-09-11 | 294.0 | CT7 | visibility_connector tokeny fourkites/shippeo. Nie live. Nastepny: paper-form source_ref /refaktor. |
| 2026-09-11 | Plan 294.0 | CT7 | visibility_connector tokeny fourkites/shippeo, nie live. Delta zaakceptowana (`/noc`). Nastepny: kod 294.0. |
| 2026-09-11 | 293.0 | UI | `/refaktor`: `CatalogSourceRefHintField` na cash/kreptd/party-doc. Nie mixin. Następny: leftover CT/pin Plan. |
| 2026-09-11 | 292.0 | UI | `/refaktor`: `CatalogSourceRefField` na carbon/free-time/telematics. Nie mixin. Następny: leftover CT/pin Plan. |
| 2026-09-11 | 291.0 | CT1 | HITL promote ASN → shipment (`asn_id`). Nie auto przy POST asn. |
| 2026-09-11 | 290.0 | CT4 | Matching lane/mode na shipment przy block_409 + etykiety HITL. |
| 2026-09-11 | 289.0 | CT4 | Matching lane/mode na ASN przy block_409 + katalog match. Nie matching na shipment. |
| 2026-09-11 | 288.0 | CT4 | HITL `routing_guide_match` guide_code_only/lane/mode. Nie silnik. |
| 2026-09-11 | 287.0 | CT4 | 409 na POST shipment gdy block_409 bez znanego guide_code. |
| 2026-09-11 | 286.0 | CT4 | Żywy HTTP 409 na ASN poza `routing_guide` przy `block_409`. Nie 409 na shipment. |
| 2026-09-11 | 285.0 | CT4 | HITL `routing_guide_enforcement` record_only/block_409. Nie żywy 409 na shipment. |
| 2026-09-11 | 284.0 | CT11 | HITL `collaboration_mark` shipper/carrier/consignee. Nie wspólny SELECT. |
| 2026-09-11 | 283.0 | CT10 | HITL `freight_audit_mark` expected_vs_invoice/charge. Nie SQL vs charge. Nie druga marża. |
| 2026-09-11 | 282.0 | CT12 | HITL `capa_mark` capa/eight_d/recurrence. Nie workflow CAPA. |
| 2026-09-11 | 281.0 | CT6 | HITL `sap_connector` sap/oracle. Nie live SOAP. Nie sekrety. |
| 2026-09-11 | 280.0 | CT3 | HITL otif_mark zakres pickup/delivery/sku. Nie OTIF%. Nie scoring SQL. |
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
| 2026-09-02 | Plan 51.0 | U-oklch-dark | delta `docs/deltas/archived/51.0-oklch-dark.md` + spec. Tokeny oklch + `.dark`. Następny: `/plaster` 51.0. |
| 2026-09-02 | 51.0 | U-oklch-dark | tokeny `oklch` + `.dark` w `index.css`. Nie tabela, nie nowa trasa. |
| 2026-09-02 | Plan 52.0 | U-money-align | delta `docs/deltas/archived/52.0-money-align.md` + spec. Oś dziesiętna `<Money/>`. Następny: `/plaster` 52.0. |
| 2026-09-02 | 52.0 | U-money-align | `<Money/>` siatka integer/ułamek/ISO. Nie float, nie grouping. |
| 2026-09-02 | Plan 53.0 | U-condensed | delta `docs/deltas/archived/53.0-table-condensed.md` + spec. Condensed tylko na `/rate-lines`. Następny: `/plaster` 53.0. |
| 2026-09-02 | 53.0 | U-condensed | `allowCondensed` na gridzie stawek. Nie globalnie. |
| 2026-09-02 | Plan 54.0 | U-primitives-json | delta `docs/deltas/archived/54.0-shadcn-radix-base.md` + spec. Pin Radix. Następny: `/plaster` 54.0. |
| 2026-09-02 | 54.0 | U-primitives-json | `components.json` `base: radix`. Nie Base UI. |
| 2026-09-02 | Plan 55.0 | U-i18n-structure | delta `docs/deltas/archived/55.0-i18n-structure.md` + spec. Klucze pl. Następny: `/plaster` 55.0. |
| 2026-09-02 | 55.0 | U-i18n-structure | `t()` + katalog pl na `/quality` i `/rollout`. Nie EN. |
| 2026-09-02 | Plan 56.0 | U-playwright-axe | delta `docs/deltas/archived/56.0-playwright-axe.md` + spec. E2E+axe. Następny: `/plaster` 56.0. |
| 2026-09-02 | 56.0 | U-playwright-axe | Chromium + axe na sesji, stawkach, HITL, wycenie. Nie live accept. |
| 2026-09-02 | Plan 57.0 | U-print | delta `docs/deltas/archived/57.0-print-sheet.md` + spec. `@media print`. Następny: `/plaster` 57.0. |
| 2026-09-02 | 57.0 | U-print | `@media print` chowa chrome. Nie PDF. |
| 2026-09-02 | 58.0 | ops | Karta jakości w `/po-plastrze`. Baseline drzewa: C901 OK, dup 2,81%, ratio 0,6%, EXPLAIN wyceny Index Scan, 0 wierszy `rate_line`. Proza: `docs/operator/ścieżka-pieniędzy.md`. |
| 2026-09-02 | 59.0 | ops | Kanon 4,4–5 w PLAN. Fala E w kolejce. Etap Refaktor → `/refaktor`. Następny: Q-E1 katalogi. |
| 2026-09-02 | Plan S | ops | Fala S (pogłębienia S1…) w PLAN po Q-E4. CURRENT zostaje Q-E1. Nie F9.1 po E. |
| 2026-09-02 | 60.0 | UI | Q-E1: `/charges`, `/organization-settings`, `/rate-lines` na `catalog-parts`. Nie mixin modeli. Nie `/quotations`. Następny: Q-E2 Plan. |
| 2026-09-02 | Plan 61.0 | ops | Q-E2: testy przez Alembic + pomiar wyceny. Delta zaakceptowana (`/noc`). Nie seed 50k. Następny: `/plaster` 61.0. |
| 2026-09-02 | 61.0 | ops | Q-E2: testy przez Alembic na `omniroute_test`. EXPLAIN Index Scan, 0 wierszy `rate_line` = N/A. Następny: Q-E3 Plan. |
| 2026-09-02 | Plan 62.0 | ops | Q-E3: how-to kontrahent+katalogi + C4 context/container. Delta zaakceptowana (`/noc`). Następny: `/plaster` 62.0. |
| 2026-09-02 | 62.0 | ops | Q-E3: how-to kontrahent i katalogi zapisu; C4 context+container w ARCHITECTURE. Nie 70 stubów. Następny: Q-E4 Plan. |
| 2026-09-02 | Plan 63.0 | ops | Q-E4: STRIDE tenant+HITL + workflow CodeQL poza gate. GHAS nie claim. Następny: `/plaster` 63.0. |
| 2026-09-02 | 63.0 | ops | Q-E4: threat model tenant+HITL; CodeQL workflow poza gate. GHAS leftover. Następny: S1 Plan (nie F9.1). |
| 2026-09-02 | Plan 64.0 | M-32 | S1: `inbound_message` draft+fixture. Delta zaakceptowana (`/noc`). Nie Graph/IMAP/send. Następny: `/plaster` 64.0. |
| 2026-09-02 | 64.0 | M-32 | `inbound_message` per tenant, RLS FORCE, fixture `source_ref`, OpenFGA, GET/POST, `/mail` lista+zapis. Nie Graph/IMAP/send. Następny: S2 Plan. |
| 2026-09-02 | Plan 65.0 | M-11 | S2: `resolve_email` na `inbound_message`. Delta zaakceptowana (`/noc`). Nie IMAP/Graph. Następny: `/plaster` 65.0. |
| 2026-09-02 | 65.0 | M-11 | `resolve_email` dopina `party_id` na `inbound_message`. FK tenanta. Nie IMAP. Nie auto przy INSERT. Następny: S3 Plan. |
| 2026-09-02 | Plan 66.0 | M-20 | S3: treść `inbound_message` → extract HITL. Delta zaakceptowana (`/noc`). Nie blob, nie zapis `rate_line`. Następny: `/plaster` 66.0. |
| 2026-09-02 | 66.0 | M-20 | Treść `inbound_message` → `extract_to_draft` HITL. Przycisk na `/mail`. Nie accept, nie `rate_line` z poczty. Następny: S4 Plan. |
| 2026-09-02 | OS-2 | ops | factory_cycle na komendach, C2, E2 run_gate, podłoga jakości, bench 66.0, karty z 3× CI. Nie Auto-AGENTS. Nie S4. |
| 2026-09-02 | OS-3 | ops | Test z nowym serwisem/API, how-to albo leftover przy zapisie, delta produktu zanim kod. Nie S4. |
| 2026-09-02 | OS-4 | ops | Skaner slopu (`craft-style`) + sufit funkcji >40 linii. Nie tożsamość z człowiekiem. Nie S4. |
| 2026-09-03 | Plan 67.0 | M-28 | S4: `customer_rfq` powiązany z `inbound_message`. Delta zaakceptowana (`/noc`). Nie ślad wycen, nie silnik. Następny: `/plaster` 67.0. |
| 2026-09-03 | 67.0 | M-28 | `customer_rfq` per tenant, FK tenanta do `inbound_message`, jeden RFQ na wiadomość, `/mail`. Nie kwota. Nie silnik. Następny: S5 Plan. |
| 2026-09-03 | Plan 68.0 | M-21 | S5: istniejący silnik wyceny na `customer_rfq`. Delta zaakceptowana (`/noc`). Nie nowy silnik. LLM nie liczy. Następny: `/plaster` 68.0. |
| 2026-09-03 | 68.0 | M-21 | Istniejący silnik na `customer_rfq` (`quotation.customer_rfq_id`). Kwota ze stawki. Nie nowy silnik. Następny: S6 Plan. |
| 2026-09-03 | Plan 69.0 | M-18 | S6: ewaluacja `applies_when` w SQL. Delta zaakceptowana (`/noc`). Nie zapis marży do `charge`. Następny: `/plaster` 69.0. |
| 2026-09-03 | 69.0 | M-18 | Matching `applies_when` w SQL na `port_surcharge`. Nie zapis do `charge`. Następny: S7 Plan. |
| 2026-09-03 | Plan 70.0 | M-09 | S7: HS/CN na RFQ/wycenie. Delta zaakceptowana (`/noc`). UN z M-52 leftover. Następny: `/plaster` 70.0. |
| 2026-09-03 | 70.0 | M-09 | HS/CN z katalogu na RFQ i wycenie. Kwota nadal ze stawki. UN leftover. Następny: S8 Plan. |
| 2026-09-03 | Plan 71.0 | M-03 | S8: prefiks numeru i token szablonu w `organization_setting`. Delta zaakceptowana (`/noc`). Następny: `/plaster` 71.0. |
| 2026-09-03 | 71.0 | M-03 | Prefiks i token szablonu w allowliście. Nie licznik. Nie PDF. Następny: S9 Plan. |
| 2026-09-03 | Plan 72.0 | M-26 | S9: numer na dokumencie oferty + print 57.0. Delta zaakceptowana (`/noc`). Nie send. Następny: `/plaster` 72.0. |
| 2026-09-03 | 72.0 | M-26 | `document_number` z prefiksu w SQL. Druk 57.0. Nie send. Nie PDF. Następny: S10 Plan. |
| 2026-09-03 | Plan 73.0 | M-16 | S10: `blocks_auto` na `customer_sop`. Delta zaakceptowana (`/noc`). Nie send. Następny: `/plaster` 73.0. |
| 2026-09-03 | 73.0 | M-16 | `blocks_auto` na SOP. Draft nie blokuje. Nie send. Następny: S11 Plan. |
| 2026-09-03 | Plan 74.0 | M-71 | S11: szyna `operator_decision`. Delta zaakceptowana (`/noc`). Nie M-57. Następny: `/plaster` 74.0. |
| 2026-09-03 | 74.0 | M-71 | Szyna `operator_decision` pending/accept/reject. Nie M-57. Nie send. Następny: S12 Plan. |
| 2026-09-03 | Plan 75.0 | M-34 | S12: tabela `operator_notice`. Delta zaakceptowana (`/noc`). Nie filtr wycen. Następny: `/plaster` 75.0. |
| 2026-09-03 | 75.0 | M-34 | Tabela `operator_notice` unread/read. Nie filtr wycen. Nie send. Następny: S13 Plan. |
| 2026-09-03 | Plan 76.0 | M-57 | S13: tabela `mail_draft` obok extract. Delta zaakceptowana (`/noc`). Accept przez S11. Następny: `/plaster` 76.0. |
| 2026-09-03 | 76.0 | M-57 | Tabela `mail_draft` obok extract. Accept przez S11. Nie czat. Nie send. Następny: S14 Plan. |
| 2026-09-03 | Plan 77.0 | M-71 | S14: `lock_version` na decyzji. Delta zaakceptowana (`/noc`). Dwa Akceptuj = jeden konflikt. Następny: `/plaster` 77.0. |
| 2026-09-03 | 77.0 | M-71 | `lock_version` na decide. Dwa Akceptuj = jeden konflikt. Nie send. Następny: S15 Plan. |
| 2026-09-03 | Plan 78.0 | M-32 | S15: ingest Graph (`graph://`, `external_id`). Delta zaakceptowana (`/noc`). Nie live HTTP. Następny: `/plaster` 78.0. |
| 2026-09-03 | 78.0 | M-32 | Ingest `graph://` + `external_id` na `inbound_message`. Ten sam id = ten sam wiersz. Nie live HTTP. Nie send. Następny: S16 Plan. |
| 2026-09-03 | Plan 79.0 | M-02 | S16: outbox `inbound_message_saved`. Delta zaakceptowana (`/noc`). Nie Temporal. Następny: `/plaster` 79.0. |
| 2026-09-03 | 79.0 | M-02 | Tabela `outbox_event`, zdarzenie po zapisie wiadomości. Ten sam subject = ten sam wiersz. Nie Temporal. Następny: S17 Plan. |
| 2026-09-03 | Plan 80.0 | M-32 | S17: ingest IMAP (`imap://`, `external_id`). Delta zaakceptowana (`/noc`). Nie live skrzynka. Następny: `/plaster` 80.0. |
| 2026-09-03 | 80.0 | M-32 | Ingest `imap://` + `external_id` na `inbound_message`. Ten sam id = ten sam wiersz. Nie live skrzynka. Następny: S18 Plan. |
| 2026-09-03 | Plan 81.0 | M-33 | S18: świadomy `mailto:` po akceptacji szkicu. Delta zaakceptowana (`/noc`). Nie Graph HTTP. Następny: `/plaster` 81.0. |
| 2026-09-03 | 81.0 | M-33 | Świadomy `mailto:` po accept szkicu. `blocks_auto` nie blokuje kliknięcia. Nie Graph HTTP. Następny: S19 Plan. |
| 2026-09-03 | Plan 82.0 | M-12 | S19: tabela `network_member`. Delta zaakceptowana (`/noc`). Nie scraping. Następny: `/plaster` 82.0. |
| 2026-09-03 | 82.0 | M-12 | Tabela `network_member` RLS. Ręczny agent w sieci. Nie portal. Następny: S20 Plan. |
| 2026-09-03 | Plan 83.0 | M-30 | S20: tabela `carrier_inquiry` (buy, do `network_member`). Delta zaakceptowana (`/noc`). Nie live HTTP. Następny: `/plaster` 83.0. |
| 2026-09-03 | 83.0 | M-30 | Tabela `carrier_inquiry` RLS. Zapytanie do `network_member`, draft, bez kwoty. Nie live HTTP. Następny: S21 Plan. |
| 2026-09-03 | S21 park | M-19 | Live HTTP kanału zaparkowane — brak umowy. Nie teatr HTTP. Następny: S22 Plan. |
| 2026-09-03 | Plan 84.0 | M-31 | S22: porównanie zapisuje `charge` (buy kanał, sell wycena). Delta zaakceptowana (`/noc`). Nie odejmuj w JS. Następny: `/plaster` 84.0. |
| 2026-09-03 | 84.0 | M-31 | Porównanie zapisuje `charge`; marża z `margin()`. Nie odejmuj w JS. Następny: S23 Plan. |
| 2026-09-03 | Plan 85.0 | M-25 | S23: `negotiated_channel_quote_id` na wycenie. Delta zaakceptowana (`/noc`). Nie nowa kwota. Następny: `/plaster` 85.0. |
| 2026-09-03 | 85.0 | M-25 | Wskazanie `channel_quote` na wycenie. Nie nowa kwota. Nie zamiast `margin()`. Następny: S24 Plan. |
| 2026-09-03 | Plan 86.0 | M-29 | S24: accept oferty = `operator_decision` na `quotation`. Delta zaakceptowana (`/noc`). Nie HITL extract. Następny: `/plaster` 86.0. |
| 2026-09-03 | 86.0 | M-29 | Accept oferty przez S11 (`quotation`). Nie HITL extract. Następny: S25 Plan. |
| 2026-09-03 | Plan 87.0 | M-24 | S25: `noted_credit_review_id` na wycenie. Delta zaakceptowana (`/noc`). Nie scoring. Następny: `/plaster` 87.0. |
| 2026-09-03 | 87.0 | M-24 | Wskazanie recenzji na wycenie. Nie scoring. Następny: S26 Plan. |
| 2026-09-03 | Plan 88.0 | M-14 | S26: `bureau_attachment_ref` na recenzji. Delta zaakceptowana (`/noc`). Nie auto-limit. Następny: `/plaster` 88.0. |
| 2026-09-03 | 88.0 | M-14 | Wskazanie raportu wywiadowni na recenzji. Nie auto-limit. Nie HTTP do biura. Następny: S27 Plan. |
| 2026-09-03 | Plan 89.0 | M-53 | S27: sprawdzenie listy na `party`. Delta zaakceptowana (`/noc`). Nie auto-match. Następny: `/plaster` 89.0. |
| 2026-09-03 | 89.0 | M-53 | Sprawdzenie listy na `party`. Nie auto-match. Nie live lista. Następny: S28 Plan. |
| 2026-09-03 | Plan 90.0 | M-35 | S28: tabela `shipment` z wyceny. Delta zaakceptowana (`/noc`). Nie tracking. Następny: `/plaster` 90.0. |
| 2026-09-03 | 90.0 | M-35 | Tabela `shipment` z wyceny. Nie tracking. Nie numer. Następny: S29 Plan. |
| 2026-09-03 | Plan 91.0 | M-36 | S29: `tracking_event` na zleceniu. Delta zaakceptowana (`/noc`). Nie mapa. Następny: `/plaster` 91.0. |
| 2026-09-03 | 91.0 | M-36 | Zdarzenia trackingu na zleceniu. Nie mapa. Nie AIS. Następny: S30 Plan. |
| 2026-09-03 | Plan 92.0 | M-38 | S30: `shipment_document` na zleceniu. Delta zaakceptowana (`/noc`). Nie PDF. Następny: `/plaster` 92.0. |
| 2026-09-03 | 92.0 | M-38 | Dokumenty na zleceniu. Nie bajty. Nie PDF. Następny: S31 Plan. |
| 2026-09-03 | Plan 93.0 | M-37 | S31: `operational_exception` na zleceniu. Delta zaakceptowana (`/noc`). Nie mapa. Następny: `/plaster` 93.0. |
| 2026-09-03 | 93.0 | M-37 | Tabela wyjątków na zleceniu. Nie mapa. Nie filtr wycen. Następny: S32 Plan. |
| 2026-09-03 | Plan 94.0 | UI | S32: Watchtower lista + S11 + lazy mapa. Delta zaakceptowana (`/noc`). Nie leaflet. Następny: `/plaster` 94.0. |
| 2026-09-03 | 94.0 | UI | Wieża: wyjątki + pending S11 + leniwy panel mapy. Nie leaflet. Następny: S33 Plan. |
| 2026-09-03 | Plan 95.0 | M-39 | S33: `edi_message` na zleceniu. Delta zaakceptowana (`/noc`). Nie parser. Następny: `/plaster` 95.0. |
| 2026-09-03 | 95.0 | M-39 | Tabela komunikatu EDI na zleceniu. Nie parser. Nie live HTTP. Następny: S34 Plan. |
| 2026-09-03 | Plan 96.0 | M-40 | S34: `sales_invoice` na zleceniu. Delta zaakceptowana (`/noc`). Nie KSeF. Następny: `/plaster` 96.0. |
| 2026-09-03 | 96.0 | M-40 | Tabela faktury sprzedaży na zleceniu. Nie KSeF. Nie druga marża. Następny: S35 Plan. |
| 2026-09-03 | Plan 97.0 | M-40 | S35: `ksef_ref` na fakturze. Delta zaakceptowana (`/noc`). Nie live HTTP. Następny: `/plaster` 97.0. |
| 2026-09-03 | 97.0 | M-40 | Numer sesji KSeF na fakturze. Nie live HTTP. Nie XML. Następny: S36 Plan. |
| 2026-09-03 | Plan 98.0 | M-41 | S36: `quote_invoice_settlement` wiąże wycenę z fakturą. Delta zaakceptowana (`/noc`). Nie druga marża. Następny: `/plaster` 98.0. |
| 2026-09-03 | 98.0 | M-41 | Tabela rozliczenia wyceny z fakturą. Nie druga marża. Nie odejmowanie. Następny: S37 Plan. |
| 2026-09-03 | Plan 99.0 | M-42 | S37: `bank_payment` wiąże fakturę z rachunkiem. Delta zaakceptowana (`/noc`). Nie SEPA. Następny: `/plaster` 99.0. |
| 2026-09-03 | 99.0 | M-42 | Tabela płatności faktury na rachunek. Nie SEPA. Nie druga marża. Następny: S38 Plan. |
| 2026-09-03 | Plan 100.0 | M-43 | S38: `money_cost` wiąże płatność z kursem NBP. Delta zaakceptowana (`/noc`). Nie odsetki. Następny: `/plaster` 100.0. |
| 2026-09-03 | 100.0 | M-43 | Tabela kosztu pieniądza: płatność przy kursie NBP. Nie odsetki. Nie mnożenie. Następny: S39 Plan. |
| 2026-09-03 | Plan 101.0 | M-44 | S39: `fx_difference` wiąże wycenę z kursem NBP. Delta zaakceptowana (`/noc`). Nie przeliczenie. Następny: `/plaster` 101.0. |
| 2026-09-03 | 101.0 | M-44 | Tabela różnicy kursowej: wycena przy kursie NBP. Nie przeliczenie. Następny: S40 Plan. |
| 2026-09-03 | Plan 102.0 | M-45 | S40: `cash_flow` wiąże wycenę z płatnością. Delta zaakceptowana (`/noc`). Nie odejmowanie. Następny: `/plaster` 102.0. |
| 2026-09-03 | 102.0 | M-45 | Tabela przepływu: wycena przy płatności. Nie odejmowanie. Następny: S41 Plan. |
| 2026-09-03 | Plan 103.0 | M-46 | S41: `cost_to_serve` wiąże SOP z wyceną. Delta zaakceptowana (`/noc`). Nie suma. Następny: `/plaster` 103.0. |
| 2026-09-03 | 103.0 | M-46 | Tabela kosztu obsługi: SOP przy wycenie. Nie suma. Następny: S42 Plan. |
| 2026-09-03 | Plan 104.0 | M-47 | S42: `bookkeeping` wiąże opłatę z fakturą. Delta zaakceptowana (`/noc`). Nie JPK. Następny: `/plaster` 104.0. |
| 2026-09-03 | 104.0 | M-47 | Tabela dekretu: opłata na fakturę. Nie JPK. Nie odejmowanie. Następny: S43 Plan. |
| 2026-09-03 | Plan 105.0 | M-91 | S43: `collective_invoice` wiąże fakturę z dodatkowym zleceniem. Delta zaakceptowana (`/noc`). Nie płatność paczką. Następny: `/plaster` 105.0. |
| 2026-09-03 | 105.0 | M-91 | Tabela zbiorczej: dodatkowe zlecenie na fakturze. Nie płatność paczką. Nie JPK. Następny: S44 Plan. |
| 2026-09-03 | Plan 106.0 | M-15 | S44: `/finance` czyta faktury. Delta zaakceptowana (`/noc`). Nie narracja. Następny: `/plaster` 106.0. |
| 2026-09-03 | 106.0 | M-15 | Tablica `/finance` czyta faktury sprzedaży. Nie suma. Nie narracja. Następny: S45 Plan. |
| 2026-09-03 | Plan 107.0 | M-56 | S45: `gdpr_request` access/erasure + tombstone konta. Delta zaakceptowana (`/noc`). Nie DPIA. Następny: `/plaster` 107.0. |
| 2026-09-03 | 107.0 | M-56 | Tabela wniosku RODO + tombstone konta. Nie DPIA. Nie DELETE `app_user`. Następny: S46 Plan. |
| 2026-09-03 | Plan 108.0 | M-48 | S46: `shipment_leg` odcinek drogowy na zleceniu. Delta zaakceptowana (`/noc`). Nie mapa. Następny: `/plaster` 108.0. |
| 2026-09-03 | 108.0 | M-48 | Tabela odcinka drogowego na zleceniu. Nie mapa. Nie TMS. Następny: S47 Plan. |
| 2026-09-03 | Plan 109.0 | M-49 | S47: `shipment_leg` `rail` na zleceniu. Delta zaakceptowana (`/noc`). Nie mapa. Następny: `/plaster` 109.0. |
| 2026-09-03 | 109.0 | M-49 | Odcinek kolejowy na tej samej tabeli nogi. Nie wagon. Nie mapa. Następny: S48 Plan. |
| 2026-09-03 | Plan 110.0 | M-50 | S48: `shipment_leg` `china_rail` na zleceniu. Delta zaakceptowana (`/noc`). Nie korytarz. Następny: `/plaster` 110.0. |
| 2026-09-03 | 110.0 | M-50 | Odcinek kolej z Chin na tej samej tabeli nogi. Nie korytarz. Nie HTTP. Następny: S49 Plan. |
| 2026-09-04 | Plan 111.0 | M-51 | S49: `shipment_leg` `ocean_lcl` na zleceniu. Delta zaakceptowana (`/noc`). Nie CFS. Następny: `/plaster` 111.0. |
| 2026-09-04 | 111.0 | M-51 | Odcinek drobnicy na tej samej tabeli nogi. Nie CFS. Nie CBM. Następny: S50 Plan (park floty). |
| 2026-09-04 | Plan 112.0 | M-111 | S50 flota named park — brak jobu „własne auto”. Zero kodu. Następny: S51 Plan. |
| 2026-09-04 | Plan 113.0 | M-55 | S51: `cargo_claim` na zleceniu. Delta zaakceptowana (`/noc`). Nie kwota. Następny: `/plaster` 113.0. |
| 2026-09-04 | 113.0 | M-55 | Tabela reklamacji ładunku na zleceniu. Nie kwota. Nie scoring. Następny: S52 Plan. |
| 2026-09-04 | Plan 114.0 | M-54 | S52: `fraud_flag` na kontrahencie. Delta zaakceptowana (`/noc`). Nie scoring osoby. Następny: `/plaster` 114.0. |
| 2026-09-04 | 114.0 | M-54 | Tabela flagi oszustwa na kontrahencie. Nie scoring osoby. Nie kwota. Następny: S54 Plan (S53 Auth0 parked). |
| 2026-09-04 | Plan 115.0 | M-76 | S54 status klienta named park — brak Auth0 S53. Zero kodu. Następny: S56 Plan. |
| 2026-09-04 | Plan 116.0 | M-57 | S56: szkice `mail_draft` na wieży. Delta zaakceptowana (`/noc`). Nie czat. Następny: `/plaster` 116.0. |
| 2026-09-04 | 116.0 | M-57 | Wieża czyta `mail_draft`. Zapis zostaje na `/ai`. Nie czat. Następny: S57 Plan. |
| 2026-09-04 | Plan 117.0 | M-15 | S57: narracja po SQL na `/finance`. Delta zaakceptowana (`/noc`). LLM nie liczy. Następny: `/plaster` 117.0. |
| 2026-09-04 | 117.0 | M-15 | Narracja po SQL na `/finance`. Nie suma. Nie LLM. Następny: S58 Plan. |
| 2026-09-04 | Plan 118.0 | M-57 | S58: SOP `blocks_auto` obok szkiców na `/ai`. Delta zaakceptowana (`/noc`). Nie auto-send. Następny: `/plaster` 118.0. |
| 2026-09-04 | 118.0 | M-57 | SOP `blocks_auto` na `/ai` obok szkiców. Nie auto-send. Następny: S59 Plan. |
| 2026-09-04 | Plan 119.0 | M-68 | S59 OTel/QA/rollout named park — brak konsumenta outboxa i jobu SaaS. Zero kodu. Następny: nie zgaduj 71–212. |
| 2026-09-04 | Plan 120.0 | M-13 | S27b: decyzje oferty na karcie. Delta zaakceptowana (`/noc`). Nie scoring osoby. Następny: `/plaster` 120.0. |
| 2026-09-04 | 120.0 | M-13 | S27b: karta czyta przyjęte/odrzucone wyceny. Nie scoring osoby. Następny: leftover S11 `changed`. |
| 2026-09-04 | Plan 121.0 | M-71 | Leftover S11 `changed`. Delta zaakceptowana (`/noc`). Nie extract. Następny: `/plaster` 121.0. |
| 2026-09-04 | 121.0 | M-71 | Leftover S11: werdykt `changed` z lock. Nie extract. Następny: leftover S7 UN na RFQ. |
| 2026-09-04 | Plan 122.0 | M-52 | S7b: UN na RFQ/wycenie. Delta zaakceptowana (`/noc`). Nie LLM. Następny: `/plaster` 122.0. |
| 2026-09-04 | 122.0 | M-52 | S7b: UN na RFQ/wycenie. Nie LLM. Nie filtr stawki. Następny: leftover S12 filtr 27.0. |
| 2026-09-04 | Plan 123.0 | M-34 | S12b: filtr kind na tablicy 27.0. Delta zaakceptowana (`/noc`). Nie auto-INSERT. Następny: `/plaster` 123.0. |
| 2026-09-04 | 123.0 | M-34 | S12b: filtr kind na tablicy 27.0. Nie auto-INSERT. Następny: leftover S32 kafelki wieży. |
| 2026-09-04 | Plan 124.0 | UI | S32: liczniki na `/watchtower`. Delta zaakceptowana (`/noc`). Nie leaflet. Następny: `/plaster` 124.0. |
| 2026-09-04 | 124.0 | UI | S32: liczniki wyjątków, pending i szkiców na wieży. Nie leaflet. Nie AIS. Następny: `/refaktor` mixin modeli. |
| 2026-09-04 | 125.0 | M-10 | `/refaktor`: trzy metody PartyService ≤40 linii. Nie mixin. Następny: `/refaktor` `create_quote`. |
| 2026-09-04 | 126.0 | M-19 | `/refaktor`: `create_quote` ≤40. Sufit funkcji 0. Następny: leftover DNA `--ink`. |
| 2026-09-04 | 127.0 | UI/M-10 | leftover DNA `--ink` + `/refaktor` `_blank_to_none`. Nie mixin. Następny: named parks. |
| 2026-09-04 | 128.0 | OS | leftover context rot: PLAN bez ręcznego SHA; AGENTS M-71 z `changed`+lock. Nie konsument. Następny: named parks. |
| 2026-09-07 | Plan benchmark | OS | Benchmark Qargo+SPEED+PDF: ADR-0004, matryca `docs/analysis/`, karty pól Fali T, kolejka-propozycja, karty `_knowledge/market/`, digesty `docs/_source/benchmark/`. Kanon kolejki bez zmian. Następny: named parks (bez zmian). |
| 2026-09-07 | Plan §13g | OS | Hub telematyczny: zero własnego HW (Teltonika+Queclink), BYO API + płyta, okno `trip`+N dni, widoczność giełd, zakaz scrapingu czatów. Karta `006-telematics-hub`. Kanon kolejki bez zmian. |
| 2026-09-07 | Plan §13h | OS | Pogoda pan-EU, BDO+DIWASS, blokada zlecenia po polisie/licencji, snapshot Trans.eu, katalog SENT-europa, myto EU/EFTA. Karta `007-compliance-eu`. Kanon kolejki bez zmian. |
| 2026-09-07 | Plan §13i | OS | Lejek oferty: sent/open/PDF/reply/conversion, czasy SQL, hostowany token, piksel tylko po zgodzie. Karta `008-quote-engagement`. Kanon kolejki bez zmian. |
| 2026-09-07 | Plan inwentarz | OS | Korekta §13e: nagłówki ≠ pełny PDF. Audyt `inwentarz-mc-pdf.md` + luki §13j + odrzucenia (dwa produkty, blueprint, HERE, auto-zapis). Kanon kolejki bez zmian. |
| 2026-09-07 | Plan §13k | OS | Podkłady map: darmowe on/off u użytkownika; płatne BYO u admina tenanta; instrukcja `podklady-map-admin.md`. Zakaz tile.openstreetmap.org. Kanon kolejki bez zmian. |
| 2026-09-07 | Plan §13l | OS | Adapter ERP/FK P0: Comarch Optima+XL, Symfonia WebAPI, Subiekt nexo+GT. Jeden KSeF. Zakaz SQL do bazy klienta. `erp-fk-adapter.md`. Kanon kolejki bez zmian. |
| 2026-09-07 | Plan §13l | OS | Doprecyzowanie: Omni wystawia FV; do FK idą przychodowe (`sales_invoice`) i kosztowe (`purchase_invoice`). KSeF tylko Omni. |
| 2026-09-07 | Plan §13m | OS | FV kosztowe z maila/KSeF/skanu: draft HITL, ranking zleceń SQL, shipment_ref na wychodzących, zakaz auto-link. F10. |
| 2026-09-07 | Plan §13n | OS | Wydruki sieci drobnicowych (CMR/groupage/etykieta) + skan zwrotny: QR Omni = podpięcie, bez kodu = HITL. D9. |
| 2026-09-07 | Plan §13o | OS | Słabe zdjęcia: gate + OpenCV (kadr/deskew/CLAHE/Lanczos), nie GAN. Split HITL z ramkami, pewnością i edycją. X9. |
| 2026-09-07 | Plan §13o | OS | Cel wyglądu: skaner płaski (~300 DPI, biel, bez cienia). ML Kit/VisionKit przy spuście; FV bez wymazywania plam. |
| 2026-09-07 | Plan §13p | OS | Książka nadawcza PP: EN + śledzenie REST + EPO (kto odebrał). F11. Zakaz scrapingu; imię tylko z EPO lub skanu ZPO. |
| 2026-09-07 | Plan §13p | OS | FV papierowa = kanał `paper_post` (Poczta Polska). Nie wyłącza KSeF. Bez nadania nie ma statusu wysłana. |
| 2026-09-07 | Audyt V5/C9 | OS | Spójność matryca↔kolejka: P0 GBOX/IKOL/Flotis/Wialon w V5 (nie HZ); Tronik/Logisat po umowie; C9 bez obietnicy opinii słownych ([ ] TO_VERIFY `api@trans.eu`). Kanon kolejki bez zmian. |
| 2026-09-07 | Plan §13q | OS | 42 nazwy z PDF: matryca §13q + rejestr odrzuceń (Driver Score, własny Video/FOTA, OSS/IOSS, JPK-moduł, Selenium, gwarancja slotu, benchmarki cross-tenant). Kanon kolejki bez zmian. |
| 2026-09-07 | Audyt §10 | OS | Akapit faktów po tabeli AI w `benchmark-tms-2026.md` §10: DocILE HITL vs Goddard RR + Skitka commission; PAL GSM-HARD; zakaz GAN SR; ETA=ML+MAE; Qargo −75% slogan; Copilot lab ≠ METR +19%. Kanon kolejki bez zmian. |
| 2026-09-07 | Analiza | OS | Luka HC-05: `charge` (009 + model) bez `source_ref`. P0 leftover w `kolejka-propozycja`; zdanie w benchmark §13h. Kanon PLAN/CURRENT bez zmian. |
| 2026-09-08 | Pin kolejki | OS | Operator: P0 `charge.source_ref` + Fala O (biurko ocean) + T/D/P/X/F/C/V w PLAN/CURRENT. Named parks parked. Karty `karty-pol-fala-o.md` … `v.md`. `/noc` nie startuje w tej sesji. |
| 2026-09-08 | Pin Fala I + O7/O8 + V5 dwa reżimy | OS | Incoterms/booking/odprawa (I1–I4), kraj na liście agentów, buy-desk group-by, slot = capability (T8), GPS `omni_telematic` vs 3 dni robocze, scoring = HITL+DPA. Audyt `incoterms-booking-customs-ux.md`. `/noc` nie startuje. |
| 2026-09-08 | Pin 2026-09-08c Luki i ulepszenia | OS | Cała oś U/N/A/G/G2/W/WA/Plat/Demo-1/CT/CI/EXP/K0 w PLAN. Karty u/n/a/w/g/g2/ci/ct/plat/exp. GLOSSARY + pola-wizja EXP1. Nic nie wyłączone. `/noc` bez godziny nie startuje. Pierwszy kod = P0. |
| 2026-09-08 | Plan 129.0 | M-08 | P0: `charge.source_ref` nullable stare / obowiązkowe na INSERT. Delta zaakceptowana (`/noc`). Nie myto. Następny: `/plaster` 129.0. |
| 2026-09-08 | 129.0 | M-08 | P0: `charge.source_ref`. Stare NULL; nowy INSERT wymaga pochodzenia. Nie myto. Nie F11. Następny: O0 Plan. |
| 2026-09-08 | Plan 130.0 | M-12 | O0: `network_member.party_id`. Delta zaakceptowana (`/noc`). Nie ranking. Następny: `/plaster` 130.0. |
| 2026-09-08 | 130.0 | M-12 | O0: `network_member.party_id` FK tenanta. Stare NULL; nowy członek wymaga kontrahenta. Nie ranking. Następny: M10-1 Plan. |
| 2026-09-08 | Plan 131.0 | M-10 | M10-1: ID biznesowe + unikat + 409 z linkiem. Delta zaakceptowana (`/noc`). Nie M10-2. Następny: kod 131.0. |
| 2026-09-08 | 131.0 | M-10 | M10-1: NIP/VAT-EU/EORI/DUNS unikat; nowy zapis wymaga ID; customer bez NIP = 400; 409 z linkiem. Nie M10-2. Następny: M10-2 Plan. |
| 2026-09-08 | Plan 132.0 | M-10 | M10-2: assignment + JDG + parent. Delta zaakceptowana (`/noc`). Nie trzy tabele. Następny: kod 132.0. |
| 2026-09-08 | 132.0 | M-10 | M10-2: role assignment + JDG + parent. Limit na JDG tylko HITL. Nie trzy tabele. Następny: B0a Plan. |
| 2026-09-08 | Plan 133.0 | B0a | `entity_event` append-only. Delta zaakceptowana (`/noc`). Nie B0b. Następny: kod 133.0. |
| 2026-09-08 | 133.0 | B0a | `entity_event` append-only. Kind inquiry/quote. Nie outbox. Nie B0b. Następny: O1 Plan. |
| 2026-09-08 | Plan 134.0 | M-19 | O1: `transit_days` + znaczki SQL. Delta zaakceptowana (`/noc`). Nie T7. Następny: kod 134.0. |
| 2026-09-08 | 134.0 | M-19 | O1: `transit_days` + znaczki SQL (ta sama waluta). Nie NBP. Następny: O2 Plan. |
| 2026-09-08 | Plan 135.0 | M-19 | O2: zapis oferty z `/quotations`. Delta zaakceptowana (`/noc`). Nie 1.3. Następny: kod 135.0. |
| 2026-09-08 | 135.0 | M-19 | O2: `source_ref` z user + 409 + formularz na wycenie. Nie 1.3. Następny: O3 Plan. |
| 2026-09-08 | Plan 136.0 | M-30 | O3: batch + statusy + lane. Delta zaakceptowana (`/noc`). Nie send. Następny: kod 136.0. |
| 2026-09-08 | 136.0 | M-30 | O3: batch + statusy + lane. Kwota tylko przy answered. Nie send. Następny: I0/U2 Plan. |
| 2026-09-08 | Plan 137.0 | M-21 | I0/U2: Incoterms na `quotation`. Delta zaakceptowana (`/noc`). Nie I1. Następny: kod 137.0. |
| 2026-09-08 | 137.0 | M-21 | I0/U2: Incoterms na wycenie. DAP/DDP bez miejsca = 409. Nie I1. Następny: O4 Plan. |
| 2026-09-08 | Plan 138.0 | O4 | N× `mail_draft` + ranking SQL + default N. Delta zaakceptowana (`/noc`). Nie O5. Następny: kod 138.0. |
| 2026-09-08 | 138.0 | M-57 | O4: N× mail_draft (carrier_inquiry) + ranking SQL + inquiry_default_n. Nie O5. Następny: O5 Plan. |
| 2026-09-08 | Plan 139.0 | M-13 | O5: party_lane_scorecard snapshot per lane. Delta zaakceptowana (/noc). Nie O6. Następny: kod 139.0. |
| 2026-09-08 | 139.0 | M-13 | O5: party_lane_scorecard snapshot per lane. Hint z szablonu. Nie O6. Następny: O6 Plan. |
| 2026-09-08 | Plan 140.0 | M-20 | O6: draft_kind carrier_quote + accept → channel_quote. Delta zaakceptowana (`/noc`). Nie F10. Następny: kod 140.0. |
| 2026-09-08 | 140.0 | M-20 | O6: draft_kind carrier_quote + accept API -> channel_quote. Nie F10. Następny: O7 Plan. |
| 2026-09-08 | 141.0 | M-12 | O7: filtr country_code na /networks z party. Nie O8. Nastepny: O8 Plan. |
| 2026-09-08 | Plan 142.0 | M-32 | O8: group_by party/country/status na /mail w table_view.config. Delta zaakceptowana (/noc). Nie watek. Nastepny: kod 142.0. |
| 2026-09-08 | 142.0 | M-32 | O8: group_by party/country/status na /mail w table_view.config. Nie watek. Nastepny: N5 Plan. |
| 2026-09-08 | Plan 143.0 | M-30 | N5: no_reply_after na carrier_inquiry + reczny notice no_reply. Delta zaakceptowana (/noc). Nie U4. Nastepny: kod 143.0. |
| 2026-09-08 | 143.0 | M-30 | N5: no_reply_after + reczny notice no_reply. Nie U4. Nastepny: U1+U5 Plan. |
| 2026-09-08 | Plan 144.0 | U1+U5 | carry-forward (3 pola Incoterms) + document_checklist_rule. Delta zaakceptowana (/noc). Nie I1. Nastepny: kod 144.0. |
| 2026-09-08 | 144.0 | U1+U5 | field_carry_forward + document_checklist_rule. Nie C8. Nastepny: I1 Plan. |
| 2026-09-08 | Plan 145.0 | I1 | incoterm_responsibility (11x2 Omni ops, nie cytat ICC). Delta zaakceptowana (/noc). Nie I2. Nastepny: kod 145.0. |
| 2026-09-08 | 145.0 | I1 | incoterm_responsibility 11x2 Omni ops, nie cytat ICC. Nie I2. Nastepny: I2 Plan. |
| 2026-09-08 | Plan 146.0 | I2 | shipment_stakeholder (7 rol z karty I2, party_id wymagane). Delta zaakceptowana (/noc). Nie EXP1. Nastepny: kod 146.0. |
| 2026-09-08 | 146.0 | I2 | shipment_stakeholder 7 rol, party_id wymagane. Nie EXP1. Nie I3. Nastepny: I3 Plan. |
| 2026-09-08 | Plan 147.0 | I3 | document_dispatch_rule (adresat, nie send). Delta zaakceptowana (`/noc`). Nie I4. Następny: kod 147.0. |
| 2026-09-08 | 147.0 | I3 | document_dispatch_rule katalog adresata. Nie send. Nie I4. Nastepny: I4 Plan. |
| 2026-09-08 | Plan 148.0 | I4 | booking_instruction (scope+rola, nie S21). Delta zaakceptowana (`/noc`). Nie U4. Nastepny: kod 148.0. |
| 2026-09-08 | 148.0 | I4 | booking_instruction na zleceniu. Nie S21. Nastepny: U4 Plan. |
| 2026-09-08 | Plan 149.0 | U4 | organization_calendar + is_working_day SQL. Delta zaakceptowana (`/noc`). Nie V5. Nastepny: kod 149.0. |
| 2026-09-08 | 149.0 | U4 | organization_calendar + is_working_day SQL. Nie V5. Nastepny: T1 Plan. |
| 2026-09-08 | Plan 150.0 | T1 | stop na zleceniu (location+strefa, nie mapa). Delta zaakceptowana (`/noc`). Nie T2. Nastepny: kod 150.0. |
| 2026-09-08 | 150.0 | T1 | stop na zleceniu (location+strefa). Nie mapa. Nastepny: T2 Plan. |
| 2026-09-08 | 151.0 | T2 | resource katalog floty (pojazd/kierowca/naczepa). Nie trip. Nastepny: T2 trip Plan. |
| 2026-09-08 | Plan 152.0 | T2 | trip (status+opcjonalny resource, nie km). Delta zaakceptowana (`/noc`). Nie T3. Nastepny: kod 152.0. |
| 2026-09-08 | 152.0 | T2 | trip status+opcjonalny resource. Nie km. Nastepny: T3 Plan. |
| 2026-09-08 | Plan 153.0 | T3 | container ISO 6346 + iso_size_type, nie VGM. Delta zaakceptowana (`/noc`). Nie T4. Nastepny: kod 153.0. |
| 2026-09-08 | Plan 154.0 | U3 | air shipment_leg + airport flag, nie HAWB. Delta zaakceptowana (`/noc`). Nie D. Nastepny: kod 154.0. |
| 2026-09-08 | 154.0 | U3 | air shipment_leg + airport flag. Nie HAWB. Nastepny: D1 Plan. |
| 2026-09-08 | Plan 155.0 | D1 | groupage_line cutoff+TT+ISODOW, nie WMS. Delta zaakceptowana (`/noc`). Nie D2. Nastepny: kod 155.0. |
| 2026-09-08 | 155.0 | D1 | groupage_line cutoff+TT+ISODOW. Nie WMS. Nastepny: D2 Plan. |
| 2026-09-08 | Plan 156.0 | D2 | shipment_package + skan QR Omni + stop trasy, nie WMS. Delta zaakceptowana (`/noc`). Nie D3. Nastepny: kod 156.0. |
| 2026-09-08 | 156.0 | D2 | shipment_package + skan QR Omni + stop trasy. Nie WMS. Nastepny: D3 Plan. |
| 2026-09-08 | Plan 157.0 | D3 | dock_appointment okno na stop magazynu, nie WMS. Delta zaakceptowana (`/noc`). Nie D4. Nastepny: kod 157.0. |
| 2026-09-08 | 157.0 | D3 | dock_appointment okno TIME na stop magazynu. Nie WMS. Nastepny: D4 Plan. |
| 2026-09-08 | Plan 158.0 | D4 | cod_instruction znacznik pobrania bez kwoty, nie F. Delta zaakceptowana (`/noc`). Nie D5. Nastepny: kod 158.0. |
| 2026-09-08 | 158.0 | D4 | cod_instruction znacznik pobrania bez kwoty. Nie F. Nastepny: D5 Plan. |
| 2026-09-08 | Plan 159.0 | D5 | groupage_tariff próg wagi na strefie, nie silnik P1. Delta zaakceptowana (`/noc`). Nie D6. Nastepny: kod 159.0. |
| 2026-09-08 | 159.0 | D5 | groupage_tariff próg wagi na strefie Decimal. Nie silnik P1. Nastepny: D6 Plan. |
| 2026-09-08 | Plan 160.0 | D6 | ocean_bill znacznik HBL/MBL na zleceniu, nie booking. Delta zaakceptowana (`/noc`). Nie D7. Nastepny: kod 160.0. |
| 2026-09-08 | 160.0 | D6 | ocean_bill znacznik HBL/MBL na zleceniu. Nie booking. Nastepny: D7 Plan. |
| 2026-09-08 | Plan 161.0 | D7 | pallet_balance saldo Chep/LPR na party, nie giełda. Delta zaakceptowana (`/noc`). Nie D8. Nastepny: kod 161.0. |
| 2026-09-08 | 161.0 | D7 | pallet_balance saldo Chep/LPR integer na party. Nie giełda. Nastepny: D9 Plan (D8 parked). |
| 2026-09-08 | Plan 162.0 | D9 | document_template layout jako dane, nie PDF. Delta zaakceptowana (`/noc`). Nie D8. Nastepny: kod 162.0. |
| 2026-09-08 | 162.0 | D9 | document_template layout jako dane. Nie PDF. Nastepny: P1 Plan (D9 leftover D9b–f). |
| 2026-09-08 | Plan 163.0 | P1 | rate_card warunek jako dane + Decimal, nie silnik WHEN. Delta zaakceptowana (`/noc`). Nie P2. Nastepny: kod 163.0. |
| 2026-09-08 | 163.0 | P1 | rate_card applies_when jako dane + Decimal. Nie silnik WHEN. Nastepny: P2 Plan. |
| 2026-09-08 | Plan 164.0 | P2 | charge_template kolekcja kodów + daty jako dane, nie exclusion. Delta zaakceptowana (`/noc`). Nie P3. Nastepny: kod 164.0. |
| 2026-09-08 | 164.0 | P2 | charge_template kolekcja kodów + daty jako dane. Nie exclusion. Nastepny: P3 Plan. |
| 2026-09-08 | Plan 165.0 | P3 | fuel_index katalog FSC/BAF/CAF obok nbp_rate, nie mnożenie na charge. Delta zaakceptowana (`/noc`). Nie P4. Nastepny: kod 165.0. |
| 2026-09-08 | 165.0 | P3 | fuel_index katalog FSC/BAF/CAF Decimal obok nbp_rate. Nie mnożenie na charge. Nastepny: P4 Plan. |
| 2026-09-08 | Plan 166.0 | P4 | local_charge THC/ISPS jako dane + Decimal, nie warning braków. Delta zaakceptowana (`/noc`). Nie P5. Nastepny: kod 166.0. |
| 2026-09-08 | 166.0 | P4 | local_charge katalog THC/ISPS Decimal. Nie warning braków. Nastepny: P5 Plan. |
| 2026-09-08 | Plan 167.0 | P5 | expected_buy snapshot na trip przy in_transit, nie wariancja. Delta zaakceptowana (`/noc`). Nie P6. Nastepny: kod 167.0. |
| 2026-09-08 | 167.0 | P5 | expected_buy freeze Decimal na trip przy in_transit. Nie wariancja. Nastepny: P6 Plan. |
| 2026-09-08 | Plan 168.0 | P6 | tender_quote ważność + limit orderów, nie auto-award. Delta zaakceptowana (`/noc`). Nie G2. Nastepny: kod 168.0. |
| 2026-09-08 | 168.0 | P6 | tender_quote ważność + limit orderów integer. Nie auto-award. Nastepny: G2.0 Plan. |
| 2026-09-08 | Plan 169.0 | G2.0 | tender nagłówek sell/buy jako dane, nie loty. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 169.0. |
| 2026-09-08 | 169.0 | G2.0 | tender nagłówek sell/buy jako dane. Nie loty. Nie auto-award. Nastepny: G2.1 Plan. |
| 2026-09-08 | Plan 170.0 | G2.1 | tender_lot kod partii na tender, nie korytarz. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 170.0. |
| 2026-09-08 | 170.0 | G2.1 | tender_lot kod partii na tender. Nie korytarz. Nie auto-award. Nastepny: G2.2 Plan. |
| 2026-09-09 | Plan 171.0 | G2.2 | tender_lane para UN/LOCODE na tender_lot, nie runda. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 171.0. |
| 2026-09-09 | 171.0 | G2.2 | tender_lane para UN/LOCODE na tender_lot. Nie runda. Nie auto-award. Nastepny: G2.3 Plan. |
| 2026-09-09 | Plan 172.0 | G2.3 | tender_round numer rundy na tender, nie data room. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 172.0. |
| 2026-09-09 | 172.0 | G2.3 | tender_round numer rundy na tender. Nie data room. Nie auto-award. Nastepny: G2.4 Plan. |
| 2026-09-09 | Plan 173.0 | G2.4 | tender_data_room NDA na tender, nie extract. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 173.0. |
| 2026-09-09 | 173.0 | G2.4 | tender_data_room NDA na tender. Nie extract. Nie auto-award. Nastepny: G2.5 Plan. |
| 2026-09-09 | Plan 174.0 | G2.5 | tender_matrix_cell kwota Decimal z P, nie LLM. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 174.0. |
| 2026-09-09 | 174.0 | G2.5 | tender_matrix_cell kwota Decimal z P na tender. Nie LLM. Nie druga marża. Nastepny: G2.6 Plan. |
| 2026-09-09 | Plan 175.0 | G2.6 | tender_playbook twierdzenie + source_ref, nie extract RFP. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 175.0. |
| 2026-09-09 | 175.0 | G2.6 | tender_playbook twierdzenie + source_ref na tender. Nie extract RFP. Nie kwota. Nastepny: G2.7 Plan. |
| 2026-09-09 | Plan 176.0 | G2.7 | tender_win_loss wynik + source_ref, nie extract RFP. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 176.0. |
| 2026-09-09 | 176.0 | G2.7 | tender_win_loss wynik + source_ref na tender. Nie extract RFP. Nie four-eyes. Nastepny: G2.8 Plan. |
| 2026-09-09 | Plan 177.0 | G2.8 | tender_consortium_member fotel + source_ref, nie extract RFP. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 177.0. |
| 2026-09-09 | 177.0 | G2.8 | tender_consortium_member fotel + source_ref na tender. Nie extract RFP. Nie TED. Nastepny: G2.9 Plan. |
| 2026-09-09 | Plan 178.0 | G2.9 | tender_rfp_intake HITL + source_ref, nie zapis z LLM. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 178.0. |
| 2026-09-09 | 178.0 | G2.9 | tender_rfp_intake HITL + source_ref na tender. Nie zapis z LLM. Nie auto-award. Nastepny: G2.9b Plan. |
| 2026-09-09 | Plan 179.0 | G2.9b | draft_kind=tender_rfp + accept HITL do intake. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 179.0. |
| 2026-09-09 | 179.0 | G2.9b | draft_kind=tender_rfp + accept HITL do tender_rfp_intake. Nie zapis z LLM. Nie auto-award. Nastepny: G2.10 Plan. |
| 2026-09-09 | Plan 180.0 | G2.10 | tender_prospect HITL + source_ref, nie scrape. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 180.0. |
| 2026-09-09 | 180.0 | G2.10 | tender_prospect HITL + source_ref na tender i party. Nie scrape. Nie bid/no-bid. Nastepny: G2.11 Plan. |
| 2026-09-09 | Plan 181.0 | G2.11 | tender_bid_stance HITL bid/no-bid, nie win/loss. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 181.0. |
| 2026-09-09 | 181.0 | G2.11 | tender_bid_stance HITL bid/no-bid + source_ref na tender. Nie win/loss. Nie auto-award. Nastepny: G2.12 Plan. |
| 2026-09-09 | Plan 182.0 | G2.12 | tender_award_review HITL cztery oczy, nie auto-award. Delta zaakceptowana (`/noc`). Nie TED scrape. Nastepny: kod 182.0. |
| 2026-09-09 | 182.0 | G2.12 | tender_award_review HITL countersign/challenge + source_ref na tender. Nie auto-award. Nie win/loss. Nastepny: G2.13 Plan. |
| 2026-09-09 | Plan 183.0 | G2.13 | tender_ted_notice HITL numer TED, nie scrape. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 183.0. |
| 2026-09-09 | 183.0 | G2.13 | tender_ted_notice HITL numer ogłoszenia TED + source_ref na tender. Nie scrape. Nie live HTTP. Nastepny: G2.14 Plan. |
| 2026-09-09 | Plan 184.0 | G2.14 | tender_carbon_mark HITL declared/exempt, nie kalkulator kg. Delta zaakceptowana (`/noc`). Nie auto-award. Nastepny: kod 184.0. |
| 2026-09-09 | 184.0 | G2.14 | tender_carbon_mark HITL declared/exempt + source_ref na tender. Nie kalkulator kg. Nie CBAM. Nastepny: leftover G2.15–G2.18 Plan. |
| 2026-09-09 | Plan 185.0 | G2.19 | lane_pattern HITL para UN/LOCODE, nie circle_sim. Delta zaakceptowana (`/noc`). Nie kalkulator kg. Nastepny: kod 185.0. |
| 2026-09-09 | 185.0 | G2.19 | lane_pattern HITL para UN/LOCODE + source_ref. Nie circle_sim. Nie km. Nastepny: leftover G2.20–G2.22 Plan. |
| 2026-09-09 | Plan 186.0 | G2.23 | kreptd_licence HITL numer licencji, nie scrape. Delta zaakceptowana (`/noc`). Nie Citizen API. Nastepny: kod 186.0. |
| 2026-09-09 | 186.0 | G2.23 | kreptd_licence HITL numer licencji + source_ref na party. Nie scrape. Nie Citizen API. Nastepny: leftover G2.20–G2.22 Plan. |
| 2026-09-09 | Plan 187.0 | C7 | monitoring_scheme HITL katalog, nie SENT XML. Delta zaakceptowana (`/noc`). Nie live PUESC. Nastepny: kod 187.0. |
| 2026-09-09 | 187.0 | C7 | monitoring_scheme HITL kod schematu + source_ref. Nie SENT XML. Nie live PUESC. Nastepny: leftover G2.20–G2.22 Plan. |
| 2026-09-09 | Plan 188.0 | C8 | party_document HITL rodzaj dokumentu na party, nie 409. Delta zaakceptowana (`/noc`). Nie extract. Nastepny: kod 188.0. |
| 2026-09-09 | 188.0 | C8 | party_document HITL kind + source_ref na party. Nie 409. Nie extract. Nastepny: leftover G2.20–G2.22 Plan. |
| 2026-09-09 | Plan 189.0 | F2 | cash_discount HITL kind na fakturze, nie kwota. Delta zaakceptowana (`/noc`). Nie CAMT. Nastepny: kod 189.0. |
| 2026-09-09 | 189.0 | F2 | cash_discount HITL kind + source_ref na fakturze. Nie kwota. Nie CAMT. Nastepny: leftover F2b Plan. |
| 2026-09-09 | Plan 190.0 | C5 | carbon_method HITL GLEC/GHG + wersja, nie kalkulator kg. Delta zaakceptowana (`/noc`). Nie live HTTP. Nastepny: kod 190.0. |
| 2026-09-09 | 190.0 | C5 | carbon_method HITL kod + wersja + source_ref. Nie kg. Nie kalkulator. Nastepny: leftover C3 Plan. |
| 2026-09-09 | Plan 191.0 | EXP0.8 | cargo_claim HITL OS&D + terminy CMR, nie silnik 7/21/365. Delta zaakceptowana (`/noc`). Nie kwota. Nastepny: kod 191.0. |
| 2026-09-09 | 191.0 | EXP0.8 | cargo_claim HITL OS&D + notice/suit DATE. Nie silnik 7/21/365. Nie kwota. Nastepny: leftover C3 Plan. |
| 2026-09-09 | Plan 192.0 | EXP0.9 | dangerous_good HITL tunel ADR + SG, nie klasa z LLM. Delta zaakceptowana (`/noc`). Nastepny: kod 192.0. |
| 2026-09-09 | 192.0 | EXP0.9 | dangerous_good HITL tunel ADR + grupa SG. Nie klasa z LLM. Nie live IMO. Nastepny: leftover C3 Plan. |
| 2026-09-09 | Plan 193.0 | B0b/V1 | prediction_ledger HITL przedział + CRPS/MAE, nie silnik. Delta zaakceptowana (`/noc`). Nastepny: kod 193.0. |
| 2026-09-09 | 193.0 | B0b/V1 | prediction_ledger HITL przedział + CRPS/MAE. Nie silnik. Nie scoring osoby. Nastepny: leftover C3 Plan. |
| 2026-09-09 | Plan 194.0 | V2 | stop HITL eta_physical/eta_legal, nie GPS i nie pogoda. Delta zaakceptowana (`/noc`). Nastepny: kod 194.0. |
| 2026-09-09 | 194.0 | V2 | stop HITL dwa ETA (fizyczne/prawne). Nie GPS. Nie pogoda. Nastepny: leftover V2 pogoda Plan. |
| 2026-09-09 | Plan 195.0 | V2 | weather_observation HITL warunek + UN/LOCODE, nie Open-Meteo. Delta zaakceptowana (`/noc`). Nastepny: kod 195.0. |
| 2026-09-09 | 195.0 | V2 | weather_observation HITL warunek + stacja + czas. Nie Open-Meteo. Nie ETA. Nastepny: V3 D&D Plan. |
| 2026-09-09 | Plan 196.0 | V3 | free_time_clock HITL rodzaj + free_days, nie countdown. Delta zaakceptowana (`/noc`). Nastepny: kod 196.0. |
| 2026-09-09 | 196.0 | V3 | free_time_clock HITL rodzaj + dni wolne. Nie countdown. Nie charge. Nastepny: V5 GPS HITL Plan. |
| 2026-09-09 | Plan 197.0 | V5 | telematics_connector HITL reżim + dostawca, nie live GPS. Delta zaakceptowana (`/noc`). Nastepny: kod 197.0. |
| 2026-09-09 | 197.0 | V5 | telematics_connector HITL reżim + dostawca. Nie live GPS. Nie sekrety. Nastepny: V6 wieża Plan. |
| 2026-09-09 | Plan 198.0 | V6 | tower_impact HITL etap łańcucha + status umowy, nie EBITDA. Delta zaakceptowana (`/noc`). Nastepny: kod 198.0. |
| 2026-09-09 | 198.0 | V6 | tower_impact HITL etap łańcucha + status umowy. Nie EBITDA. Nie scoring. Nastepny: W1 twin Plan. |
| 2026-09-09 | Plan 199.0 | W1 | twin_mark HITL 8 rodzajów, nie fizyka. Delta zaakceptowana (`/noc`). Nastepny: kod 199.0. |
| 2026-09-09 | 199.0 | W1 | twin_mark HITL 8 rodzajów. Nie fizyka. Nie plan_snapshot. Nastepny: W2 war room Plan. |
| 2026-09-09 | Plan 200.0 | W2 | war_room_mark HITL rodzaj incydentu, nie N8, nie drugi czat. Delta zaakceptowana (`/noc`). Nastepny: kod 200.0. |
| 2026-09-09 | 200.0 | W2 | war_room_mark HITL rodzaj incydentu. Nie N8. Nie drugi czat. Nastepny: W3 memory graph Plan. |
| 2026-09-09 | Plan 201.0 | W3 | memory_edge HITL rodzaj krawędzi, nie RAG. Delta zaakceptowana (`/noc`). Nastepny: kod 201.0. |
| 2026-09-09 | 201.0 | W3 | memory_edge HITL rodzaj krawędzi. Nie RAG. Nie graf na entity_event. Nastepny: W4 Executive AI Plan. |
| 2026-09-09 | Plan 202.0 | W4 | executive_mark HITL rodzaj pytania zarządu, nie suma LLM. Delta zaakceptowana (`/noc`). Nastepny: kod 202.0. |
| 2026-09-09 | 202.0 | W4 | executive_mark HITL rodzaj pytania zarządu. Nie suma LLM. Nie narracja SQL. Nastepny: W5 ranking Plan. |
| 2026-09-09 | Plan 203.0 | W5 | rank_mark HITL oś rankingu, nie auto-award. Delta zaakceptowana (`/noc`). Nastepny: kod 203.0. |
| 2026-09-09 | 203.0 | W5 | rank_mark HITL oś rankingu zakupu. Nie auto-award. Nie N szkiców. Nastepny: leftover D9b Plan. |
| 2026-09-09 | Plan 204.0 | D9b | shipment_ref HITL numer zlecenia, nie QR/PDF. Delta zaakceptowana (`/noc`). Nastepny: kod 204.0. |
| 2026-09-09 | 204.0 | D9b | shipment_ref HITL twardy numer na zleceniu. Nie QR. Nie PDF. Nastepny: leftover P1b Plan. |
| 2026-09-09 | Plan 205.0 | P1b | rate_card matching GET równość SQL jak 69.0, nie parser. Delta zaakceptowana (`/noc`). Nastepny: kod 205.0. |
| 2026-09-09 | 205.0 | P1b | rate_card matching GET równość SQL. Nie parser WHEN/IF. Nastepny: leftover P2c Plan. |
| 2026-09-09 | Plan 206.0 | P2c | charge_template exclusion daterange jak 4.1, nie Python. Delta zaakceptowana (`/noc`). Nastepny: kod 206.0. |
| 2026-09-09 | 206.0 | P2c | charge_template exclusion daterange. Nie overlap w Pythonie. Nastepny: leftover P3b–d Plan. |
| 2026-09-09 | Plan 207.0 | P4b | local_charge port_unlocode HITL, nie FK geography. Delta zaakceptowana (`/noc`). Nastepny: kod 207.0. |
| 2026-09-09 | 207.0 | P4b | local_charge port_unlocode HITL. Nie FK geography. Nastepny: leftover P4b rest Plan. |
| 2026-09-09 | Plan 208.0 | P4b | local_charge iso_size_type HITL, nie FK container. Delta zaakceptowana (`/noc`). Nastepny: kod 208.0. |
| 2026-09-09 | 208.0 | P4b | local_charge iso_size_type HITL. Nie FK container. Nastepny: leftover P4c parked. |
| 2026-09-09 | Plan 209.0 | U3b | hawb_no/mawb_no HITL na shipment_leg air, nie pula IATA. Delta zaakceptowana (`/noc`). Nie ocean_bill. Nastepny: kod 209.0. |
| 2026-09-09 | 209.0 | U3b | hawb_no/mawb_no HITL na shipment_leg air. Nie pula IATA. Nie ocean_bill. Nastepny: leftover T4 parent_shipment_id Plan. |
| 2026-09-09 | Plan 210.0 | T4 | parent_shipment_id HITL FK na shipment, nie SQL na charge. Delta zaakceptowana (`/noc`). Nie N1. Nastepny: kod 210.0. |
| 2026-09-09 | 210.0 | T4 | parent_shipment_id HITL FK na shipment. Nie SQL na charge. Nie N1. Nastepny: leftover T4b parked. |
| 2026-09-09 | Plan 211.0 | T7 | fx_rate_basis HITL w organization_setting, nie mnozenie. Delta zaakceptowana (`/noc`). Nie charge. Nastepny: kod 211.0. |
| 2026-09-09 | 211.0 | T7 | fx_rate_basis HITL w organization_setting. Nie mnozenie. Nie charge. Nastepny: leftover T7b parked. |
| 2026-09-09 | Plan 212.0 | T2c | driver2_id HITL na trip, nie km i nie fleet. Delta zaakceptowana (`/noc`). Nastepny: kod 212.0. |
| 2026-09-09 | 212.0 | T2c | driver2_id HITL na trip. Nie km. Nie fleet. Nastepny: leftover T1 stop_group Plan. |
| 2026-09-09 | Plan 213.0 | T1 | stop_group_code HITL na stop, nie nowa tabela. Delta zaakceptowana (`/noc`). Nastepny: kod 213.0. |
| 2026-09-09 | 213.0 | T1 | stop_group_code HITL na stop. Nie nowa tabela. Nie mapa. Nastepny: leftover T1b parked. |
| 2026-09-09 | Plan 214.0 | T2 | route_label HITL na trip, nie km. Delta zaakceptowana (`/noc`). Nastepny: kod 214.0. |
| 2026-09-09 | 214.0 | T2 | route_label HITL na trip. Nie km. Nie fleet. Nastepny: leftover T1 notes_for_driver Plan. |
| 2026-09-09 | Plan 215.0 | T1 | notes_for_driver HITL na stop, nie waga. Delta zaakceptowana (`/noc`). Nastepny: kod 215.0. |
| 2026-09-09 | 215.0 | T1 | notes_for_driver HITL na stop. Nie waga. Nie mapa. Nastepny: leftover T3 seal_no_1 Plan. |
| 2026-09-09 | Plan 216.0 | T3 | seal_no_1 HITL na container, nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 216.0. |
| 2026-09-09 | 216.0 | T3 | seal_no_1 HITL na container. Nie PIN. Nie VGM. Nastepny: leftover T3 seal_no_2 Plan. |
| 2026-09-09 | Plan 217.0 | T3 | seal_no_2 HITL na container, nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 217.0. |
| 2026-09-09 | 217.0 | T3 | seal_no_2 HITL na container. Nie PIN. Nie VGM. Nastepny: leftover T3 seal_no_3 Plan. |
| 2026-09-09 | Plan 218.0 | T3 | seal_no_3 HITL na container, nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 218.0. |
| 2026-09-09 | 218.0 | T3 | seal_no_3 HITL na container. Nie PIN. Nie VGM. Nastepny: leftover T3 vessel_name Plan. |
| 2026-09-09 | Plan 219.0 | T3 | vessel_name HITL na container, nie rejs i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 219.0. |
| 2026-09-09 | 219.0 | T3 | vessel_name HITL na container. Nie rejs. Nie PIN. Nastepny: leftover T3 voyage_no Plan. |
| 2026-09-09 | Plan 220.0 | T3 | voyage_no HITL na container, nie booking i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 220.0. |
| 2026-09-09 | 220.0 | T3 | voyage_no HITL na container. Nie booking. Nie PIN. Nastepny: leftover T3 remarks Plan. |
| 2026-09-09 | Plan 221.0 | T3 | remarks HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 221.0. |
| 2026-09-09 | 221.0 | T3 | remarks HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 cargo_description Plan. |
| 2026-09-09 | Plan 222.0 | T3 | cargo_description HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 222.0. |
| 2026-09-09 | 222.0 | T3 | cargo_description HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 packaging_code Plan. |
| 2026-09-09 | Plan 223.0 | T3 | packaging_code HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 223.0. |
| 2026-09-09 | 223.0 | T3 | packaging_code HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 ref_1 Plan. |
| 2026-09-09 | Plan 224.0 | T3 | ref_1 HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 224.0. |
| 2026-09-09 | 224.0 | T3 | ref_1 HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 ref_2 Plan. |
| 2026-09-09 | Plan 225.0 | T3 | ref_2 HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 225.0. |
| 2026-09-09 | 225.0 | T3 | ref_2 HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 ref_3 Plan. |
| 2026-09-09 | Plan 226.0 | T3 | ref_3 HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 226.0. |
| 2026-09-09 | 226.0 | T3 | ref_3 HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 ref_4 Plan. |
| 2026-09-09 | Plan 227.0 | T3 | ref_4 HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 227.0. |
| 2026-09-09 | 227.0 | T3 | ref_4 HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 ref_5 Plan. |
| 2026-09-09 | Plan 228.0 | T3 | ref_5 HITL na container, nie waga i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 228.0. |
| 2026-09-09 | 228.0 | T3 | ref_5 HITL na container. Nie waga. Nie PIN. Nastepny: leftover T3 reefer Plan. |
| 2026-09-09 | Plan 229.0 | T3 | reefer HITL na container, nie temperatura i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 229.0. |
| 2026-09-09 | 229.0 | T3 | reefer HITL na container. Nie temperatura. Nie PIN. Nastepny: leftover T3 party/terminal Plan. |
| 2026-09-10 | Plan 230.0 | T3 | pickup_terminal HITL na container, nie FK i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 230.0. |
| 2026-09-10 | 230.0 | T3 | pickup_terminal HITL na container. Nie FK. Nie PIN. Nastepny: leftover T3 return_terminal Plan. |
| 2026-09-10 | Plan 231.0 | T3 | return_terminal HITL na container, nie FK i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 231.0. |
| 2026-09-10 | 231.0 | T3 | return_terminal HITL na container. Nie FK. Nie PIN. Nastepny: leftover T3 bl_kind Plan. |
| 2026-09-10 | Plan 232.0 | T3 | bl_kind HITL na container, nie HBL/MBL i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 232.0. |
| 2026-09-10 | 232.0 | T3 | bl_kind HITL na container. Nie HBL. Nie PIN. Nastepny: leftover T3 free_time_origin_h Plan. |
| 2026-09-10 | Plan 233.0 | T3 | free_time_origin_h HITL na container, nie countdown i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 233.0. |
| 2026-09-10 | 233.0 | T3 | free_time_origin_h HITL na container. Nie countdown. Nie PIN. Nastepny: leftover T3 free_time_dest_h Plan. |
| 2026-09-10 | Plan 234.0 | T3 | free_time_dest_h HITL na container, nie countdown i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 234.0. |
| 2026-09-10 | 234.0 | T3 | free_time_dest_h HITL na container. Nie countdown. Nie PIN. Nastepny: leftover T3 si_cutoff_at Plan. |
| 2026-09-10 | Plan 235.0 | T3 | si_cutoff_at HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 235.0. |
| 2026-09-10 | 235.0 | T3 | si_cutoff_at HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 ams_cutoff_at Plan. |
| 2026-09-10 | docs/OS | noc | Os leftoverow bez skip HITL; preflight -Helper; lista API operatora. Nastepny: Plan 236.0 ams_cutoff_at. |
| 2026-09-10 | Plan 236.0 | T3 | ams_cutoff_at HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 236.0. |
| 2026-09-10 | 236.0 | T3 | ams_cutoff_at HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 cy_cutoff_at Plan. |
| 2026-09-10 | Plan 237.0 | T3 | cy_cutoff_at HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 237.0. |
| 2026-09-10 | 237.0 | T3 | cy_cutoff_at HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 cfs_cutoff_at Plan. |
| 2026-09-10 | Plan 238.0 | T3 | cfs_cutoff_at HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 238.0. |
| 2026-09-10 | 238.0 | T3 | cfs_cutoff_at HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 VGM bundle Plan. |
| 2026-09-10 | Plan 239.0 | T3 | VGM bundle HITL na container, nie live HTTP i nie kalkulator. Delta zaakceptowana (`/noc`). Nastepny: kod 239.0. |
| 2026-09-10 | 239.0 | T3 | VGM bundle HITL na container. Nie live HTTP. Nie kalkulator. Nastepny: leftover T3 last_survey_at Plan. |
| 2026-09-10 | Plan 240.0 | T3 | last_survey_at HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 240.0. |
| 2026-09-10 | 240.0 | T3 | last_survey_at HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 booking_no Plan. |
| 2026-09-10 | Plan 241.0 | T3 | booking_no HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 241.0. |
| 2026-09-10 | 241.0 | T3 | booking_no HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 carrier_party_id Plan. |
| 2026-09-10 | Plan 242.0 | T3 | carrier_party_id HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 242.0. |
| 2026-09-10 | 242.0 | T3 | carrier_party_id HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover T3 shipment_leg_id Plan. |
| 2026-09-10 | Plan 243.0 | T3 | shipment_leg_id HITL na container, nie live HTTP i nie PIN. Delta zaakceptowana (`/noc`). Nastepny: kod 243.0. |
| 2026-09-10 | 243.0 | T3 | shipment_leg_id HITL na container. Nie live HTTP. Nie PIN. Nastepny: leftover eventy 2a/2b Plan. |
| 2026-09-10 | Plan 244.0 | B0a | inquiry_queued z API przy POST queued, nie import BC. Delta zaakceptowana (`/noc`). Nastepny: kod 244.0. |
| 2026-09-10 | 244.0 | B0a | inquiry_queued z API przy POST queued. Nie live HTTP. Nie import BC. Nastepny: leftover 2b Plan. |
| 2026-09-10 | Plan 245.0 | B0a | inquiry_sent z API przy POST sent, nie quote_recorded. Delta zaakceptowana (/noc). Nastepny: kod 245.0. |
| 2026-09-10 | 245.0 | B0a | inquiry_sent z API przy POST sent. Nie live HTTP. Nie import BC. Nastepny: leftover quote_recorded Plan. |
| 2026-09-10 | Plan 246.0 | B0a | quote_recorded z API przy POST answered, nie channel_quote. Delta zaakceptowana (`/noc`). Nastepny: kod 246.0. |
| 2026-09-10 | 246.0 | B0a | quote_recorded z API przy POST answered. Nie live HTTP. Nie import BC. Nastepny: leftover stop_group/EXP1 Plan. |
| 2026-09-10 | Plan 247.0 | T1 | weight_kg HITL na stop, nie tabela stop_group i nie VGM. Delta zaakceptowana (`/noc`). Nastepny: kod 247.0. |
| 2026-09-10 | 247.0 | T1 | weight_kg HITL na stop. Nie VGM. Nie mapa. Nastepny: leftover T1 EXP1 ilosc/plomba Plan. |
| 2026-09-10 | Plan 248.0 | T1 | quantity HITL na stop, nie opakowanie i nie plomba. Delta zaakceptowana (`/noc`). Nastepny: kod 248.0. |
| 2026-09-10 | 248.0 | T1 | quantity HITL na stop. Nie opakowanie. Nie mapa. Nastepny: leftover T1 EXP1 opakowanie/plomba Plan. |
| 2026-09-10 | Plan 249.0 | T1 | packaging_code HITL na stop, nie plomba i nie FK slownika. Delta zaakceptowana (`/noc`). Nastepny: kod 249.0. |
| 2026-09-10 | 249.0 | T1 | packaging_code HITL na stop. Nie plomba. Nie mapa. Nastepny: leftover T1 EXP1 plomba/awizacja Plan. |
| 2026-09-10 | Plan 250.0 | T1 | seal_in HITL na stop, nie seal_out i nie awizacja. Delta zaakceptowana (`/noc`). Nastepny: kod 250.0. |
| 2026-09-10 | 250.0 | T1 | seal_in HITL na stop. Nie seal_out. Nie mapa. Nastepny: leftover T1 EXP1 seal_out/awizacja Plan. |
| 2026-09-10 | Plan 251.0 | T1 | seal_out HITL na stop, nie awizacja. Delta zaakceptowana (`/noc`). Nastepny: kod 251.0. |
| 2026-09-10 | 251.0 | T1 | seal_out HITL na stop. Nie awizacja. Nie mapa. Nastepny: leftover T1 EXP1 awizacja Plan. |
| 2026-09-10 | Plan 252.0 | T1 | appointment_ref HITL na stop, nie D3 i nie waiting. Delta zaakceptowana (`/noc`). Nastepny: kod 252.0. |
| 2026-09-10 | 252.0 | T1 | appointment_ref HITL na stop. Nie D3. Nie mapa. Nastepny: leftover T1 EXP1 waiting Plan. |
| 2026-09-10 | Plan 253.0 | T1 | waiting_free_minutes HITL na stop, nie countdown i nie POD. Delta zaakceptowana (`/noc`). Nastepny: kod 253.0. |
| 2026-09-10 | 253.0 | T1 | waiting_free_minutes HITL na stop. Nie countdown. Nie mapa. Nastepny: leftover T1 EXP1 waiting_started_at Plan. |
| 2026-09-10 | Plan 254.0 | T1 | waiting_started_at HITL na stop, nie countdown i nie POD. Delta zaakceptowana (`/noc`). Nastepny: kod 254.0. |
| 2026-09-10 | 254.0 | T1 | waiting_started_at HITL na stop. Nie countdown. Nie mapa. Nastepny: leftover T1 EXP1 POD Plan. |
| 2026-09-10 | Plan 255.0 | T1 | pod_quality HITL na stop, nie kamera i nie km. Delta zaakceptowana (`/noc`). Nastepny: kod 255.0. |
| 2026-09-10 | 255.0 | T1 | pod_quality HITL na stop. Nie kamera. Nie mapa. Nastepny: leftover T2c km/fleet Plan. |
| 2026-09-10 | Plan 256.0 | T2 | planned_distance_km HITL na trip, nie actual i nie fleet. Delta zaakceptowana (`/noc`). Nastepny: kod 256.0. |
| 2026-09-10 | 256.0 | T2 | planned_distance_km HITL na trip. Nie GPS. Nie mapa. Nastepny: leftover T2c actual_distance_km Plan. |
| 2026-09-10 | Plan 257.0 | T2 | actual_distance_km HITL na trip, nie GPS i nie fleet. Delta zaakceptowana (`/noc`). Nastepny: kod 257.0. |
| 2026-09-10 | 257.0 | T2 | actual_distance_km HITL na trip. Nie GPS. Nie mapa. Nastepny: leftover T2c subcontractor_party_id Plan. |
| 2026-09-10 | Plan 258.0 | T2 | subcontractor_party_id HITL na trip, nie fleet i nie C8. Delta zaakceptowana (`/noc`). Nastepny: kod 258.0. |
| 2026-09-10 | 258.0 | T2 | subcontractor_party_id HITL na trip. Nie fleet. Nie mapa. Nastepny: leftover T2c /fleet Plan. |
| 2026-09-10 | Plan 259.0 | T2 | trasa /fleet na resource, nie GPS i nie HW. Delta zaakceptowana (`/noc`). Nastepny: kod 259.0. |
| 2026-09-10 | 259.0 | T2 | trasa /fleet na resource. Nie GPS. Nie HW. Nastepny: leftover N1 consignment Plan. |
| 2026-09-10 | Plan 260.0 | N1 | consignment HITL na shipment, N wierszy, nie FTL unique i nie mapa. Delta zaakceptowana (`/noc`). Nastepny: kod 260.0. |
| 2026-09-10 | 260.0 | N1 | consignment HITL na shipment. N wierszy. Nie mapa. Nastepny: leftover T6 mapa Plan. |
| 2026-09-10 | Plan 261.0 | T6 | trasa /planning + mapa lazy na trip, nie GPS i nie 4 widoki. Delta zaakceptowana (`/noc`). Nastepny: kod 261.0. |
| 2026-09-10 | 261.0 | T6 | /planning leniwy overlay trip. Nie GPS. Nie 4 widoki. Nastepny: leftover T4b SQL charge Plan. |
| 2026-09-10 | Plan 262.0 | T4 | marża listy charge z SQL, nie kolumna i nie rollup drzewa. Delta zaakceptowana (`/noc`). Nastepny: kod 262.0. |
| 2026-09-10 | 262.0 | T4 | GET listy charge: marża sell−buy w SQL. Nie kolumna. Nie rollup. Nastepny: leftover lookup/KSeF TE Plan. |
| 2026-09-10 | Plan 263.0 | T5 | task_template HITL kod + applies_when, nie instancja i nie outbox. Delta zaakceptowana (`/noc`). Nastepny: kod 263.0. |
| 2026-09-10 | 263.0 | T5 | task_template HITL kod + applies_when. Nie instancja. Nie outbox. Nastepny: leftover outbox T5 Plan. |
| 2026-09-10 | Plan 264.0 | T5 | outbox task_template_saved na istniejacej tabeli, nie konsument i nie worker. Delta zaakceptowana (`/noc`). Nastepny: kod 264.0. |
| 2026-09-10 | 264.0 | T5 | outbox task_template_saved. Nie konsument. Nie worker. Nastepny: leftover plan_snapshot Plan. |
| 2026-09-10 | Plan 265.0 | B0b | plan_snapshot HITL trojka UUID bez FK, nie kolka i nie what-if. Delta zaakceptowana (/noc). Nastepny: kod 265.0. |
| 2026-09-10 | 265.0 | B0b | plan_snapshot HITL trojka UUID bez FK. Nie kolka. Nie what-if. Nastepny: leftover kolka / circle_sim Plan. |
| 2026-09-10 | Plan 266.0 | G2.20 | circle_sim HITL kod + para UN/LOCODE unload/load, nie silnik 500k. Delta zaakceptowana (`/noc`). Nastepny: kod 266.0. |
| 2026-09-10 | 266.0 | G2.20 | circle_sim HITL kod + para UN/LOCODE unload/load. Nie silnik 500k. Nie km. Nastepny: leftover km ladowny/pusty/dolot Plan. |
| 2026-09-10 | Plan 267.0 | G2.21 | lane_km HITL ladowny/pusty/dolot Decimal, nie Haversine i nie trip. Delta zaakceptowana (`/noc`). Nastepny: kod 267.0. |
| 2026-09-10 | 267.0 | G2.21 | lane_km HITL ladowny/pusty/dolot Decimal. Nie Haversine. Nie trip. Nastepny: leftover F9 Optima fixture Plan. |
| 2026-09-10 | Plan 268.0 | F9 | erp_connector HITL kod + kind optima, nie live SOAP. Delta zaakceptowana (`/noc`). Nastepny: kod 268.0. |
| 2026-09-10 | 268.0 | F9 | erp_connector HITL kod + kind optima. Nie live SOAP. Nie sekrety. Nastepny: leftover T8 Plan. |
| 2026-09-10 | Plan 269.0 | T8 | terminal_slot_connector HITL mode + godziny N4, nie booking i nie confirmed z formularza. Delta zaakceptowana (`/noc`). Nastepny: kod 269.0. |
| 2026-09-10 | 269.0 | T8 | terminal_slot_connector HITL mode + godziny N4. Nie live T8. Nie confirmed z formularza. Nastepny: leftover S53 Auth0 Plan. |
| 2026-09-10 | Plan 270.0 | S53 | idp_connector HITL Auth0 fixture, nie login i nie live HTTP. Delta zaakceptowana (`/noc`). Nastepny: kod 270.0. |
| 2026-09-10 | 270.0 | S53 | idp_connector HITL token auth0. Nie login. Nie live Auth0. Nastepny: leftover portale/diada S55 / Fala X Plan. |
| 2026-09-10 | Plan 271.0 | S55 | exchange_connector HITL kod + kind trans_eu, nie live giełda. Delta zaakceptowana (`/noc`). Nastepny: kod 271.0. |
| 2026-09-10 | 271.0 | S55 | exchange_connector HITL kind trans_eu. Nie live giełda. Nie SPA. Nastepny: leftover CT7/CI9 / reszta pinu Plan. |
| 2026-09-10 | Plan 272.0 | CI9 | customer_contract HITL nagłówek kod + etykiety, nie ciphertext i nie CT7 live. Delta zaakceptowana (`/noc`). Nastepny: kod 272.0. |
| 2026-09-10 | 272.0 | CI9 | customer_contract HITL nagłówek kod + etykiety. Nie treść. Nie ciphertext. Nastepny: leftover CI9 ciphertext/KEK albo CT7 parked live Plan. |
| 2026-09-10 | Plan 273.0 | CI9 | customer_contract HITL opaque BYTEA present/absent, nie szyfr. Delta zaakceptowana (`/noc`). Nastepny: kod 273.0. |
| 2026-09-10 | 273.0 | CI9 | customer_contract HITL opaque blob present/absent. Nie szyfr. Nie KEK. Nastepny: leftover CI9 KEK mark albo CT7 parked live Plan. |
| 2026-09-10 | Plan 274.0 | CI9 | tenant_contract_kek HITL znacznik owijki, nie klucz. Delta zaakceptowana (`/noc`). Nastepny: kod 274.0. |
| 2026-09-10 | 274.0 | CI9 | tenant_contract_kek HITL wrap_kind password/kms. Nie klucz. Nie materiał. Nastepny: leftover CT7 parked live / reszta pinu Plan. |
| 2026-09-10 | Plan 275.0 | CT7 | visibility_connector HITL kod + kind p44, nie live track. Delta zaakceptowana (`/noc`). Nastepny: kod 275.0. |
| 2026-09-10 | 275.0 | CT7 | visibility_connector HITL kind p44. Nie live track. Nie AIS. Nastepny: leftover CT1 purchase_order / reszta pinu Plan. |
| 2026-09-10 | Plan 276.0 | CT1 | purchase_order HITL nagłówek kod + opcjonalny zakład. Delta zaakceptowana (`/noc`). Nastepny: kod 276.0. |
| 2026-09-10 | 276.0 | CT1 | purchase_order HITL nagłówek. Nie po_line. Nie ASN. Nastepny: leftover CT1 po_line / ASN / reszta pinu Plan. |
| 2026-09-10 | Plan 277.0 | CT1 | po_line HITL linia SKU + qty Decimal + JM. Delta zaakceptowana (`/noc`). Nastepny: kod 277.0. |
| 2026-09-10 | 277.0 | CT1 | po_line HITL linia SKU + qty Decimal. Nie ASN. Nastepny: leftover CT1 ASN / reszta pinu Plan. |
| 2026-09-11 | Plan 278.0 | CT1 | asn HITL awizo na PO. Delta zaakceptowana (`/noc`). Nastepny: kod 278.0. |
| 2026-09-11 | 278.0 | CT1 | asn HITL awizo na PO. Nie live EDI. Nie auto shipment. Nastepny: leftover auto shipment / reszta pinu Plan. |
| 2026-09-11 | Plan 279.0 | CT4 | routing_guide HITL katalog. Auto shipment/CT2 parked z powodem. Delta zaakceptowana (`/noc`). Nastepny: kod 279.0. |
| 2026-09-11 | 279.0 | CT4 | routing_guide HITL katalog. Nie 409. Nastepny: leftover CT / pin Plan. |
