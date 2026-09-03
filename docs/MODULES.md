# Rejestr modułów (skrót)

Pełny rejestr, plastry i zależności:  
`Informacje z claude/REJESTR-MODULOW-I-PLAN-v2.md` — **nie dumpować** do kontekstu.

Numeracja plastrów w kodzie: **0.3 = RLS**, **0.4 = OpenFGA** (nie outbox), **0.5 = Frontend Shell** (nie konfiguracja).

## Fundament i AI (to, co istnieje w kodzie)

| ID | Moduł | Plaster | Status |
|---|---|---|---|
| M-01 | Wielodostępność / tenancy | 0.3 RLS + 0.4 OpenFGA + 0.12 JWT + 0.15 hasła | **ukończony (fundament)** · Auth0 I1/I2 **odroczone** (brak tenanta); sesja email+hasło+JWT ≠ IdP |
| M-20 | Ekstrakcja dokumentów | 0.7–0.14 HITL + T0 + 0.18 live HTTP PG + 1.3 accept→rate_line + U-art50 + U-pdf-spans + 2.1–2.2 · 66.0 z `inbound_message` | **ukończony (fundament)** · HTTP = live PG; ExtractionService nie importuje rates ani inbound |
| M-02 | Outbox / idempotencja | 79.0 `outbox_event` | **ukończony (fundament)** · `inbound_message_saved` po zapisie wiadomości; nie Temporal; nie konsument |
| M-03 | Konfiguracja jako dane | 3.0 `organization_setting` · 71.0 prefiks/szablon | **ukończony (fundament)** · allowlista; nie sekrety; numer oferty w 72.0 |
| M-06 | charge_code + aliasy | 1.0 katalog | **ukończony (fundament)** · aliasy na wierszu; nie `rate_line` / `charge` |
| M-07 | rate_line (stawka kupna) | 1.1 immutable + source_ref | **ukończony (fundament)** · nie `charge` / marża |
| M-08 | charge (buy+sell, marża) | 1.2 jeden wiersz | **ukończony (fundament)** · nie accept HITL (1.3) |
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` · 5.1 POL/POD + `party_id` · 16.0 odczyt `nbp_rate` · 20.0 wsad kodów · 68.0 `customer_rfq_id` | **ukończony (fundament)** · nie marża; nie k6; nie override; nie nowy silnik |
| M-05 | Geografia | 4.0 `port` + 4.1 `location`/strefy + 4.2 `terminal`/WPI | **ukończony (fundament)** · `operator_party_id` od 5.0; `operator_name` zostaje |
| M-10 | Kontrahenci | 5.0 `party` + katalog zależny | **ukończony (fundament)** · lookup = szkic/fixture; override nie karmić wyceny |
| M-09 | Kody towarowe | 5.2 `commodity_code` · 70.0 FK na RFQ/wycenie | **ukończony (fundament)** · nie IMDG; UN z M-52 leftover |
| M-23 | Kurs NBP | 6.0 `nbp_rate` · 16.0 odczyt przy `quotation` | **ukończony (fundament)** · nie przeliczenie kwoty; nie żywe M-07 `rate_line` |
| M-52 | Towary niebezpieczne | 7.0 `dangerous_good` | **ukończony (fundament)** · nie podpięcie do wyceny; nie żywe M-08 `charge` |
| M-11 | Automatyczne kontakty | 8.0 `resolve_email` | **ukończony (fundament)** · matcher domeny z 5.0; nie IMAP; nie portal |
| M-12 | Sieci i stowarzyszenia | 9.0 `network` · 82.0 `network_member` | **ukończony (fundament)** · katalog sieci + ręczni członkowie; nie portal WCA |
| M-13 | Karta wyników kontrahenta | 10.0 `party_scorecard` | **ukończony (fundament)** · snapshot karty; nie SQL-refresh; nie scoring osoby |
| M-16 | Procedury operacyjne klienta | 11.0 `customer_sop` · 73.0 `blocks_auto` | **ukończony (fundament)** · zatwierdzona SOP może blokować auto; nie send; nie S11 |
| M-18 | Opłaty portowe warunkowe | 12.0 `port_surcharge` · 69.0 matching `applies_when` | **ukończony (fundament)** · katalog extra + SQL równość warunku; nie zapis do `charge`; nie parser AST |
| M-19 | Stawki live i kanały | 13.0 `channel_quote` | **ukończony (fundament)** · katalog oferty; nie live HTTP; nie zapis do `rate_line` / `charge` |
| M-14 | Ocena kredytowa | 14.0 `credit_review` · 88.0 `bureau_attachment_ref` | **ukończony (fundament)** · katalog recenzji + wskazanie raportu; nie auto-scoring; nie zapis `credit_limit` |
| M-15 | Wirtualny Dyrektor Finansowy | 15.0 `finance_board` · 106.0 FV | **ukończony (S44)** · tablica odczytu `/finance` + faktury; nie silnik; LLM nie liczy |
| M-24 | Ryzyko oferty | 17.0 `offer_risk` · 87.0 wskazanie | **ukończony (fundament)** · odczyt + `noted_credit_review_id`; nie scoring; nie auto-limit |
| M-25 | Negocjacja i wynik | 18.0 `offer_negotiation` · 85.0 wskazanie | **ukończony (fundament)** · odczyt + `negotiated_channel_quote_id`; nie won/lost; nie spread |
| M-26 | Dokument oferty | 19.0 `offer_document` · 72.0 `document_number` | **ukończony (fundament)** · numer z prefiksu; druk 57.0; nie PDF; nie send |
| M-27 | Wycena wsadowa | 20.0 `quotation_batch` | **ukończony (fundament)** · wiele kodów na lane; nie CSV; nie nowa tabela |
| M-28 | Zapytania od klientów | 21.0 `customer_inquiry` · 67.0 `customer_rfq` | **ukończony (fundament)** · ślad wycen + obiekt RFQ; silnik = M-21 68.0; nie IMAP |
| M-29 | Wykrywanie akceptacji | 22.0 `offer_acceptance` · 86.0 S11 | **ukończony (fundament)** · pending + decyzja na `quotation`; nie HITL accept; nie CSV |
| M-30 | Zapytania do agentów/armatorów | 23.0 ślad · 83.0 `carrier_inquiry` | **ukończony (fundament)** · obiekt buy do `network_member`; ślad `channel_quote` przy lane; nie RFQ; nie live HTTP |
| M-31 | Porównanie odpowiedzi | 24.0 ślad · 84.0 `charge` | **ukończony (fundament)** · zestawienie na POL/POD + zapis marży w `charge`; nie odejmuj w JS; nie won/lost |
| M-32 | Integracja pocztowa | 64.0 `inbound_message` · 66.0 extract HITL · 78.0 ingest `graph://` · 80.0 ingest `imap://` | **ukończony (fundament)** · tabela wiadomości draft+fixture albo ingest Graph/skrzynka po `external_id` na `/mail`; treść → szkic HITL; nie live skrzynka; nie send; nie blob |
| M-33 | Dodatek do Outlooka | 26.0 `mail_client` · 81.0 dispatch `mailto:` | **ukończony (fundament)** · `mailto:` kontaktu na `/mail` + świadoma wysyłka zaakceptowanego szkicu na `/ai`; nie Office.js; nie Graph HTTP |
| M-34 | Powiadomienia | 27.0 tablica · 75.0 tabela `operator_notice` | **ukończony (fundament)** · inbox zapisany + leftover filtr pending; nie send |
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
| M-55 | Reklamacja ładunku | 113.0 `cargo_claim` | **plan (S51)** · reklamacja na zleceniu; nie kwota; nie scoring |
| M-56 | RODO | 46.0 `gdpr` · 107.0 `gdpr_request` | **ukończony (fundament)** · wniosek access/erasure + tombstone konta; nie DPIA; nie DELETE `app_user` |
| M-57 | Copilot AI | 47.0 `ai_copilot` · 76.0 `mail_draft` | **ukończony (fundament)** · pending extract + szkic maila; 81.0 send na M-33; nie czat |
| M-68 | Obserwowalność | 48.0 `observability` | **ukończony (fundament)** · tablica `fetchHealth`; nie OTel; nie k6 |
| M-69 | Jakość | 49.0 `extraction_quality` | **ukończony (fundament)** · tablica `unparsed_regions`; nie scoring; nie tabela QA |
| M-70 | Wdrożenie | 50.0 `tenant_rollout` | **ukończony (fundament)** · tablica `default_currency`; nie tabela rollout; nie upsert |
| M-71 | Szyna decyzji operatora | 74.0 `operator_decision` · 77.0 lock | **ukończony (fundament)** · pending → accept/reject + `lock_version`; nie extract 1.3; nie send |

Nie dopisuj tu 70 pustych wierszy M-xx. Katalog + **kolejka Q1… / Q-E / Fala S** (co budować jedno po drugim, tryb Plan potem plaster): `docs/PLAN-REALIZACJA.md` § Kolejka. Archiwum Claude zostaje magazynem specyfikacji, nie SoT kolejności.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`, `rate-line.md`, `charge.md`, `quotation.md`, `organization-setting.md`, `geography.md` (4.0–4.2 w kodzie), `parties.md` (5.0 + 8.0 matcher maila w kodzie), `commodity-code.md` (5.2 w kodzie), `nbp-rate.md` (6.0 w kodzie), `dangerous-good.md` (7.0 w kodzie), `network.md` (9.0 w kodzie), `party-scorecard.md` (10.0 w kodzie), `customer-sop.md` (11.0 w kodzie), `port-surcharge.md` (12.0 w kodzie), `channel-quote.md` (13.0 w kodzie), `credit-review.md` (14.0 w kodzie), `finance-board.md` (15.0 w kodzie), `operator-decision.md` (74.0 w kodzie), `operator-notice.md` (27.0 + 75.0 w kodzie), `ai-copilot.md` (47.0 + 76.0 w kodzie). Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
