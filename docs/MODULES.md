# Rejestr modułów (skrót)

Pełny rejestr, plastry i zależności:  
`Informacje z claude/REJESTR-MODULOW-I-PLAN-v2.md` — **nie dumpować** do kontekstu.

Numeracja plastrów w kodzie: **0.3 = RLS**, **0.4 = OpenFGA** (nie outbox), **0.5 = Frontend Shell** (nie konfiguracja).

## Fundament i AI (to, co istnieje w kodzie)

| ID | Moduł | Plaster | Status |
|---|---|---|---|
| M-01 | Wielodostępność / tenancy | 0.3 RLS + 0.4 OpenFGA + 0.12 JWT + 0.15 hasła | **ukończony (fundament)** · Auth0 I1/I2 **odroczone** (brak tenanta); sesja email+hasło+JWT ≠ IdP |
| M-20 | Ekstrakcja dokumentów | 0.7–0.14 HITL + T0 + 0.18 live HTTP PG + 1.3 accept→rate_line + U-art50 + U-pdf-spans + 2.1–2.2 · 66.0 z `inbound_message` | **ukończony (fundament)** · HTTP = live PG; ExtractionService nie importuje rates ani inbound |
| M-02 | Outbox / idempotencja | 79.0 `outbox_event` · 264.0 `task_template_saved` | **ukończony (fundament)** · dwa kindy; nie Temporal; nie konsument |
| M-03 | Konfiguracja jako dane | 3.0 `organization_setting` · 71.0 prefiks/szablon | **ukończony (fundament)** · allowlista; nie sekrety; numer oferty w 72.0 |
| M-06 | charge_code + aliasy | 1.0 katalog | **ukończony (fundament)** · aliasy na wierszu; nie `rate_line` / `charge` |
| M-07 | rate_line (stawka kupna) | 1.1 immutable + source_ref | **ukończony (fundament)** · nie `charge` / marża |
| M-08 | charge (buy+sell, marża) | 1.2 jeden wiersz · 129.0 `source_ref` | **ukończony (fundament + P0)** · nie accept HITL (1.3) |
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` · 5.1 POL/POD + `party_id` · 16.0 odczyt `nbp_rate` · 20.0 wsad kodów · 68.0 `customer_rfq_id` | **ukończony (fundament)** · nie marża; nie k6; nie override; nie nowy silnik |
| M-05 | Geografia | 4.0 `port` + 4.1 `location`/strefy + 4.2 `terminal`/WPI | **ukończony (fundament)** · `operator_party_id` od 5.0; `operator_name` zostaje |
| M-10 | Kontrahenci | 5.0 `party` + 131.0 ID · 132.0 role/JDG/parent | **ukończony (fundament + M10-1/M10-2)** · lookup = szkic/fixture; override nie karmić wyceny |
| M-09 | Kody towarowe | 5.2 `commodity_code` · 70.0 FK na RFQ/wycenie | **ukończony (fundament)** · nie IMDG |
| M-52 | Towary niebezpieczne | 7.0 `dangerous_good` · 122.0 FK · 192.0 tunel ADR + SG | **ukończony (leftover S7b + EXP0.9 HITL)** · UN + tunel + SG; nie LLM; nie live IMO |
| M-23 | Kurs NBP | 6.0 `nbp_rate` · 16.0 odczyt przy `quotation` | **ukończony (fundament)** · nie przeliczenie kwoty; nie żywe M-07 `rate_line` |
| M-11 | Automatyczne kontakty | 8.0 `resolve_email` | **ukończony (fundament)** · matcher domeny z 5.0; nie IMAP; nie portal |
| M-12 | Sieci i stowarzyszenia | 9.0 `network` · 82.0 `network_member` · 130.0 `party_id` | **ukończony (fundament + O0)** · członek wiąże kontrahenta; nie portal WCA |
| M-13 | Karta wyników kontrahenta | 10.0 `party_scorecard` · 120.0 decyzje oferty | **ukończony (leftover S27b)** · odczyt przyjętych/odrzuconych wycen; nie scoring osoby; SQL-refresh lane = kolejka **O5** |
| M-16 | Procedury operacyjne klienta | 11.0 `customer_sop` · 73.0 `blocks_auto` | **ukończony (fundament)** · zatwierdzona SOP może blokować auto; nie send; nie S11 |
| M-18 | Opłaty portowe warunkowe | 12.0 `port_surcharge` · 69.0 matching `applies_when` | **ukończony (fundament)** · katalog extra + SQL równość warunku; nie zapis do `charge`; nie parser AST |
| M-19 | Stawki live i kanały | 13.0 `channel_quote` | **ukończony (fundament)** · katalog oferty; nie live HTTP; TT + ręczny wpis z wyceny = kolejka **O1/O2** |
| M-14 | Ocena kredytowa | 14.0 `credit_review` · 88.0 `bureau_attachment_ref` | **ukończony (fundament)** · katalog recenzji + wskazanie raportu; nie auto-scoring; nie zapis `credit_limit` |
| M-15 | Wirtualny Dyrektor Finansowy | 15.0 `finance_board` · 106.0 FV · 117.0 narracja | **ukończony (S57)** · narracja po SQL na `/finance`; nie silnik; LLM nie liczy |
| M-24 | Ryzyko oferty | 17.0 `offer_risk` · 87.0 wskazanie | **ukończony (fundament)** · odczyt + `noted_credit_review_id`; nie scoring; nie auto-limit |
| M-25 | Negocjacja i wynik | 18.0 `offer_negotiation` · 85.0 wskazanie | **ukończony (fundament)** · odczyt + `negotiated_channel_quote_id`; nie won/lost; nie spread |
| M-26 | Dokument oferty | 19.0 `offer_document` · 72.0 `document_number` | **ukończony (fundament)** · numer z prefiksu; druk 57.0; nie PDF; nie send |
| M-27 | Wycena wsadowa | 20.0 `quotation_batch` | **ukończony (fundament)** · wiele kodów na lane; nie CSV; nie nowa tabela |
| M-28 | Zapytania od klientów | 21.0 `customer_inquiry` · 67.0 `customer_rfq` | **ukończony (fundament)** · ślad wycen + obiekt RFQ; silnik = M-21 68.0; nie IMAP |
| M-29 | Wykrywanie akceptacji | 22.0 `offer_acceptance` · 86.0 S11 | **ukończony (fundament)** · pending + decyzja na `quotation`; nie HITL accept; nie CSV |
| M-30 | Zapytania do agentów/armatorów | 23.0 ślad · 83.0 `carrier_inquiry` | **ukończony (fundament)** · jeden `draft` do `network_member`; batch + statusy + lane = kolejka **O3/O4** |
| M-31 | Porównanie odpowiedzi | 24.0 ślad · 84.0 `charge` | **ukończony (fundament)** · zestawienie na POL/POD + zapis marży w `charge`; nie odejmuj w JS; nie won/lost |
| M-32 | Integracja pocztowa | 64.0 `inbound_message` · 66.0 extract HITL · 78.0 ingest `graph://` · 80.0 ingest `imap://` | **ukończony (fundament)** · tabela wiadomości draft+fixture albo ingest Graph/skrzynka po `external_id` na `/mail`; treść → szkic HITL; nie live skrzynka; nie send; nie blob |
| M-33 | Dodatek do Outlooka | 26.0 `mail_client` · 81.0 dispatch `mailto:` | **ukończony (fundament)** · `mailto:` kontaktu na `/mail` + świadoma wysyłka zaakceptowanego szkicu na `/ai`; nie Office.js; nie Graph HTTP |
| M-34 | Powiadomienia | 27.0 tablica · 75.0 tabela · 123.0 filtr pending | **ukończony (leftover S12b)** · filtr kind na tablicy; nie auto-INSERT; nie send |
| M-35 | Zlecenie | 90.0 `shipment` | **ukończony (S28)** · tabela z wyceny; nie tracking |
| M-36 | Tracking | 91.0 `tracking_event` | **ukończony (S29)** · zdarzenia na zleceniu; nie mapa |
| M-37 | Wyjątki | 93.0 `operational_exception` | **ukończony (S31)** · tabela na zleceniu; nie AIS; nie mapa |
| M-38 | Dokumenty zlecenia | 92.0 `shipment_document` | **ukończony (S30)** · wskazanie na zleceniu; nie bajty; nie PDF |
| M-39 | EDI | 95.0 `edi_message` | **ukończony (S33)** · tabela na zleceniu; nie parser; nie live HTTP |
| M-40 | Fakturowanie i KSeF | 33.0 tablica · 96.0 `sales_invoice` · 97.0 `ksef_ref` | **ukończony (S35)** · numer sesji na fakturze; nie live HTTP; nie druga marża |
| M-41 | Rozliczenie wyceny z fakturą | 34.0 tablica · 98.0 `quote_invoice_settlement` | **ukończony (S36)** · para wycena+faktura; nie druga marża |
| M-42 | Bank i płatności | 35.0 tablica · 99.0 `bank_payment` | **ukończony (S37)** · para faktura+rachunek; nie SEPA |
| M-43 | Koszt pieniądza | 36.0 tablica · 100.0 `money_cost` | **ukończony (S38)** · para płatność+kurs NBP; nie odsetki |
| M-44 | Różnice kursowe | 37.0 tablica · 101.0 `fx_difference` | **ukończony (S39)** · para wycena+kurs NBP; nie przeliczenie |
| M-45 | Przepływy | 38.0 tablica · 102.0 `cash_flow` | **ukończony (S40)** · para wycena+płatność; nie odejmowanie |
| M-46 | Koszt obsługi klienta | 39.0 tablica · 103.0 `cost_to_serve` | **ukończony (S41)** · para SOP+wycena; nie suma |
| M-47 | Księgowość (integracja) | 40.0 tablica · 104.0 `bookkeeping` | **ukończony (S42)** · para opłata+faktura; nie JPK |
| M-91 | Zbiorcza faktura | 105.0 `collective_invoice` | **ukończony (S43)** · para faktura+dodatkowe zlecenie; nie płatność paczką |
| M-48 | Transport drogowy | 41.0 `road_transport` · 108.0 `shipment_leg` | **ukończony (S46)** · odcinek `road` na zleceniu; nie TMS; nie mapa |
| M-49 | Kolej intermodalna | 42.0 `intermodal_rail` · 109.0 `shipment_leg` rail | **ukończony (S47)** · odcinek `rail` na zleceniu; nie wagon; nie mapa |
| M-50 | Kolej z Chin | 43.0 `china_rail` · 110.0 `shipment_leg` china_rail | **ukończony (S48)** · odcinek kolej z Chin na zleceniu; nie korytarz; nie HTTP |
| M-51 | Drobnica morska | 44.0 `ocean_lcl` · 111.0 `shipment_leg` ocean_lcl | **ukończony (S49)** · odcinek drobnicy na zleceniu; nie tabela LCL; nie CFS |
| M-53 | Sankcje | 45.0 `sanctions` · 89.0 `sanctions_list_ref` | **ukończony (fundament)** · tablica + sprawdzenie na `party`; nie auto-match; nie live lista |
| M-54 | Oszustwo | 114.0 `fraud_flag` | **ukończony (S52)** · flaga na kontrahencie; nie scoring osoby; nie kwota |
| M-55 | Reklamacja ładunku | 191.0 `cargo_claim` | **ukończony (S51 + EXP0.8 HITL)** · OS&D + terminy CMR; nie kwota; nie silnik 7/21/365 |
| M-56 | RODO | 46.0 `gdpr` · 107.0 `gdpr_request` | **ukończony (fundament)** · wniosek access/erasure + tombstone konta; nie DPIA; nie DELETE `app_user` |
| M-57 | Copilot AI | 47.0 `ai_copilot` · 76.0 `mail_draft` · 116.0 wieża · 118.0 SOP | **ukończony (S58)** · szkice po SOP `blocks_auto`; nie auto-send; nie czat |
| M-68 | Obserwowalność | 48.0 `observability` · 119.0 park | **ukończony (fundament)** · tablica `fetchHealth`; S59 named park; nie OTel; nie k6 |
| M-69 | Jakość | 49.0 `extraction_quality` | **ukończony (fundament)** · tablica `unparsed_regions`; nie scoring; nie tabela QA |
| M-70 | Wdrożenie | 50.0 `tenant_rollout` | **ukończony (fundament)** · tablica `default_currency`; nie tabela rollout; nie upsert |
| M-71 | Szyna decyzji operatora | 74.0 `operator_decision` · 77.0 lock · 121.0 `changed` | **ukończony (leftover S11b)** · pending → accept/changed/reject + `lock_version`; nie extract 1.3; nie send |
| B0b | Ledger predykcji | 193.0 `prediction_ledger` · 265.0 `plan_snapshot` | **ukończony (HITL)** · przedział + CRPS/MAE + wersja planu; leftover champion / drift |
| G2.20 | Kółko HITL | 266.0 `circle_sim` | **ukończony (HITL)** · kod + para unload/load; leftover silnik 500k / km / P |
| G2.21 | Km ładowny HITL | 267.0 `lane_km` | **ukończony (HITL)** · ładowny/pusty/dolot Decimal; leftover P / silnik 500k |
| F9 | Konektor Optima HITL | 268.0 `erp_connector` | **ukończony (HITL)** · kod + kind `optima`; leftover XL / live SOAP / FS+FZ |
| T8 | Konektor slotu HITL | 269.0 `terminal_slot_connector` | **ukończony (HITL)** · mode + godziny N4; leftover live API / `terminal_appointment` / confirmed |
| S53 | Konektor IdP HITL | 270.0 `idp_connector` | **ukończony (HITL)** · kod + provider `auth0`; leftover I1/I2 live / portale |
| S55 | Konektor giełdy HITL | 271.0 `exchange_connector` | **ukończony (HITL)** · kod + kind `trans_eu`; leftover live giełda / X1–X5 SPA |
| CI9 | Umowa klienta HITL | 272.0 `customer_contract` | **ukończony (HITL nagłówek)** · kod + etykiety; leftover ciphertext / KEK |
| V2 | Pogoda HITL | 194.0 `stop` ETA · 195.0 `weather_observation` | **ukończony (HITL)** · dwa ETA + warunek/stacja; leftover Open-Meteo / myto |
| V3 | Zegar D&D HITL | 196.0 `free_time_clock` | **ukończony (HITL)** · rodzaj + dni wolne; leftover countdown / charge / blank sailing |
| V5 | Konektor GPS HITL | 197.0 `telematics_connector` | **ukończony (HITL)** · reżim + dostawca; leftover position_event / ciphertext / 3 dni U4 |
| V6 | Impact wieży HITL | 198.0 `tower_impact` | **ukończony (HITL)** · etap łańcucha + status umowy; leftover silnik EBITDA / sla_clause / scoring |
| W1 | Bliźniak HITL | 199.0 `twin_mark` | **ukończony (HITL)** · 8 rodzajów; leftover 8 silników fizyki (`plan_snapshot` DONE 265.0) |
| W2 | Sala kryzysowa HITL | 200.0 `war_room_mark` | **ukończony (HITL)** · rodzaj incydentu; leftover N8 / T8 live API / widok sklejony |
| W3 | Krawędź pamięci HITL | 201.0 `memory_edge` | **ukończony (HITL)** · rodzaj krawędzi; leftover graf / pgvector / RAG na stawkach |
| W4 | Pytanie zarządu HITL | 202.0 `executive_mark` | **ukończony (HITL)** · rodzaj pytania; leftover suma LLM / zdania SQL |
| W5 | Oś rankingu HITL | 203.0 `rank_mark` | **ukończony (HITL)** · oś zakupu; leftover ranking SQL / N szkiców / auto-award |

Nie dopisuj tu 70 pustych wierszy M-xx. Katalog + **kolejka Q1… / Q-E / Fala S** (co budować jedno po drugim, tryb Plan potem plaster): `docs/PLAN-REALIZACJA.md` § Kolejka. Archiwum Claude zostaje magazynem specyfikacji, nie SoT kolejności.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`, `rate-line.md`, `charge.md`, `quotation.md`, `organization-setting.md`, `geography.md` (4.0–4.2 w kodzie), `parties.md` (5.0 + 8.0 matcher maila w kodzie), `commodity-code.md` (5.2 w kodzie), `nbp-rate.md` (6.0 w kodzie), `dangerous-good.md` (7.0 w kodzie), `network.md` (9.0 w kodzie), `party-scorecard.md` (10.0 w kodzie), `customer-sop.md` (11.0 w kodzie), `port-surcharge.md` (12.0 w kodzie), `channel-quote.md` (13.0 w kodzie), `credit-review.md` (14.0 w kodzie), `finance-board.md` (15.0 w kodzie), `operator-decision.md` (74.0 w kodzie), `operator-notice.md` (27.0 + 75.0 w kodzie), `ai-copilot.md` (47.0 + 76.0 w kodzie). Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
