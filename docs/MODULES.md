# Rejestr modułów (skrót)

Pełny rejestr, plastry i zależności:  
`Informacje z claude/REJESTR-MODULOW-I-PLAN-v2.md` — **nie dumpować** do kontekstu.

Numeracja plastrów w kodzie: **0.3 = RLS**, **0.4 = OpenFGA** (nie outbox), **0.5 = Frontend Shell** (nie konfiguracja).

## Fundament i AI (to, co istnieje w kodzie)

| ID | Moduł | Plaster | Status |
|---|---|---|---|
| M-01 | Wielodostępność / tenancy | 0.3 RLS + 0.4 OpenFGA + 0.12 JWT + 0.15 hasła | **ukończony (fundament)** · Auth0 I1/I2 **odroczone** (brak tenanta); sesja email+hasło+JWT ≠ IdP |
| M-20 | Ekstrakcja dokumentów | 0.7–0.14 HITL + T0 + 0.18 live HTTP PG + 1.3 accept→rate_line + U-art50 + U-pdf-spans + 2.1–2.2 | **ukończony (fundament)** · HTTP = live PG; ExtractionService nie importuje rates |
| M-02 | Outbox / idempotencja | nie 0.4 | planowany · **nie startować** (brak zdarzeń między BC) |
| M-03 | Konfiguracja jako dane | 3.0 `organization_setting` | **ukończony (fundament)** · allowlista; nie sekrety; nie env |
| M-06 | charge_code + aliasy | 1.0 katalog | **ukończony (fundament)** · aliasy na wierszu; nie `rate_line` / `charge` |
| M-07 | rate_line (stawka kupna) | 1.1 immutable + source_ref | **ukończony (fundament)** · nie `charge` / marża |
| M-08 | charge (buy+sell, marża) | 1.2 jeden wiersz | **ukończony (fundament)** · nie accept HITL (1.3) |
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` · 5.1 POL/POD + `party_id` · 16.0 odczyt `nbp_rate` · 20.0 wsad kodów | **ukończony (fundament)** · nie marża; nie k6; nie override; nie mnożenie kwoty |
| M-05 | Geografia | 4.0 `port` + 4.1 `location`/strefy + 4.2 `terminal`/WPI | **ukończony (fundament)** · `operator_party_id` od 5.0; `operator_name` zostaje |
| M-10 | Kontrahenci | 5.0 `party` + katalog zależny | **ukończony (fundament)** · lookup = szkic/fixture; override nie karmić wyceny |
| M-09 | Kody towarowe | 5.2 `commodity_code` | **ukończony (fundament)** · nie podpięcie do wyceny; nie IMDG |
| M-23 | Kurs NBP | 6.0 `nbp_rate` · 16.0 odczyt przy `quotation` | **ukończony (fundament)** · nie przeliczenie kwoty; nie żywe M-07 `rate_line` |
| M-52 | Towary niebezpieczne | 7.0 `dangerous_good` | **ukończony (fundament)** · nie podpięcie do wyceny; nie żywe M-08 `charge` |
| M-11 | Automatyczne kontakty | 8.0 `resolve_email` | **ukończony (fundament)** · matcher domeny z 5.0; nie IMAP; nie portal |
| M-12 | Sieci i stowarzyszenia | 9.0 `network` | **ukończony (fundament)** · katalog sieci; nie `network_member`; nie scraping |
| M-13 | Karta wyników kontrahenta | 10.0 `party_scorecard` | **ukończony (fundament)** · snapshot karty; nie SQL-refresh; nie scoring osoby |
| M-16 | Procedury operacyjne klienta | 11.0 `customer_sop` | **ukończony (fundament)** · katalog + zatwierdzenie; nie generator zadań; nie M-35 |
| M-18 | Opłaty portowe warunkowe | 12.0 `port_surcharge` | **ukończony (fundament)** · katalog extra; nie zapis do `charge`; nie ewaluacja warunku |
| M-19 | Stawki live i kanały | 13.0 `channel_quote` | **ukończony (fundament)** · katalog oferty; nie live HTTP; nie zapis do `rate_line` / `charge` |
| M-14 | Ocena kredytowa | 14.0 `credit_review` | **ukończony (fundament)** · katalog recenzji; nie auto-scoring; nie zapis `credit_limit` |
| M-15 | Wirtualny Dyrektor Finansowy | 15.0 `finance_board` | **ukończony (fundament)** · tablica odczytu `/finance`; nie silnik AI; LLM nie liczy |
| M-24 | Ryzyko oferty | 17.0 `offer_risk` | **ukończony (fundament)** · odczyt recenzji i karty przy `/quotations`; nie scoring; nie nowa tabela |
| M-25 | Negocjacja i wynik | 18.0 `offer_negotiation` | **ukończony (fundament)** · odczyt `channel_quote` przy `/quotations`; nie wynik won/lost; nie spread |
| M-26 | Dokument oferty | 19.0 `offer_document` | **ukończony (fundament)** · podgląd faktów `quotation`; nie PDF; nie U-print |
| M-27 | Wycena wsadowa | 20.0 `quotation_batch` | **ukończony (fundament)** · wiele kodów na lane; nie CSV; nie nowa tabela |
| M-28 | Zapytania od klientów | 21.0 `customer_inquiry` | **ukończony (fundament)** · ślad wycen per party; nie tabela RFQ; nie IMAP |
| M-29 | Wykrywanie akceptacji | 22.0 `offer_acceptance` | **ukończony (fundament)** · pending z wycen; nie tabela wyniku; nie HITL accept |
| M-30 | Zapytania do agentów/armatorów | 23.0 `carrier_inquiry` | **ukończony (fundament)** · ślad `channel_quote` przy lane; nie RFQ; nie live HTTP |
| M-31 | Porównanie odpowiedzi | 24.0 `response_comparison` | **ukończony (fundament)** · zestawienie kwot na POL/POD; nie tabela; nie spread |
| M-32 | Integracja pocztowa | 25.0 `mail_integration` | **ukończony (fundament)** · tablica znanych adresów; nie IMAP; nie tabela skrzynki |
| M-33 | Dodatek do Outlooka | 26.0 `mail_client` | **ukończony (fundament)** · `mailto:` na `/mail`; nie Office.js; nie Graph |
| M-34 | Powiadomienia | 27.0 `operator_notice` | **ukończony (fundament)** · tablica HITL i wycen pending; nie tabela; nie wysyłka |
| M-35 | Zlecenie | 28.0 `shipment` | **ukończony (fundament)** · tablica wycen z `party_id`; nie tabela; nie tracking |
| M-36 | Tracking | 29.0 `tracking` | **ukończony (fundament)** · tablica lane POL/POD; nie tabela; nie mapa |
| M-37 | Wyjątki | 30.0 `operational_exception` | **ukończony (fundament)** · tablica wycen z party bez pełnego POL/POD; nie tabela; nie AIS |
| M-38 | Dokumenty zlecenia | 31.0 `shipment_document` | **ukończony (fundament)** · tablica `source_ref` wycen z party; nie tabela; nie PDF |
| M-39 | EDI | 32.0 `edi_message` | **ukończony (fundament)** · tablica `channel_quote` na lane wyceny; nie tabela; nie X12 |
| M-40 | Fakturowanie i KSeF | 33.0 `sales_invoice` | **ukończony (fundament)** · tablica `sell` z `charge`; nie tabela; nie KSeF |
| M-41 | Rozliczenie wyceny z fakturą | 34.0 `quote_invoice_settlement` | **ukończony (fundament)** · tablica wycena + `sell` po `rate_line_id`; nie tabela; nie odejmowanie |
| M-42 | Bank i płatności | 35.0 `bank_payment` | **ukończony (fundament)** · tablica IBAN + `sell` z `charge`; nie tabela płatności; nie SEPA |
| M-43 | Koszt pieniądza | 36.0 `money_cost` | **ukończony (fundament)** · tablica NBP + `buy` z `charge`; nie tabela odsetek; nie mnożenie |
| M-44 | Różnice kursowe | 37.0 `fx_difference` | **ukończony (fundament)** · tablica NBP walut z `charge`/`quotation`; nie tabela; nie przeliczenie |
| M-45 | Przepływy | 38.0 `cash_flow` | **ukończony (fundament)** · tablica `buy`/`sell` jako wypływ/wpływ; nie tabela księgi; nie odejmowanie |
| M-46 | Koszt obsługi klienta | 39.0 `cost_to_serve` | **ukończony (fundament)** · tablica SOP + wyceny kontrahenta; nie tabela ABC; nie suma |
| M-47 | Księgowość (integracja) | 40.0 `bookkeeping` | **ukończony (fundament)** · tablica `charge` + nazwa kodu; nie JPK; nie ERP |
| M-48 | Transport drogowy | 41.0 `road_transport` | **ukończony (fundament)** · tablica `postal_zone`/`address`; nie TMS; nie GPS |
| M-49 | Kolej intermodalna | 42.0 `intermodal_rail` | **ukończony (fundament)** · tablica portów z flagą `rail`; nie wagon; nie CIM |
| M-50 | Kolej z Chin | 43.0 `china_rail` | **ukończony (fundament)** · tablica portów CN z flagą `rail`; nie korytarz; nie HTTP |
| M-51 | Drobnica morska | 44.0 `ocean_lcl` | **ukończony (fundament)** · tablica portów `is_seaport`; nie tabela LCL; nie CFS |
| M-53 | Sankcje | 45.0 `sanctions` | **ukończony (fundament)** · tablica aktywnych party tax_id/kraj; nie OFAC; nie HTTP |
| M-56 | RODO | 46.0 `gdpr` | **ukończony (fundament)** · tablica emaili `app_user`; nie wniosek; nie usuwanie |

Nie dopisuj tu 70 pustych wierszy M-xx. Katalog + **kolejka Q1…** (co budować jedno po drugim, tryb Plan potem plaster): `docs/PLAN-REALIZACJA.md` § Kolejka. Archiwum Claude zostaje magazynem specyfikacji, nie SoT kolejności.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`, `rate-line.md`, `charge.md`, `quotation.md`, `organization-setting.md`, `geography.md` (4.0–4.2 w kodzie), `parties.md` (5.0 + 8.0 matcher maila w kodzie), `commodity-code.md` (5.2 w kodzie), `nbp-rate.md` (6.0 w kodzie), `dangerous-good.md` (7.0 w kodzie), `network.md` (9.0 w kodzie), `party-scorecard.md` (10.0 w kodzie), `customer-sop.md` (11.0 w kodzie), `port-surcharge.md` (12.0 w kodzie), `channel-quote.md` (13.0 w kodzie), `credit-review.md` (14.0 w kodzie), `finance-board.md` (15.0 w kodzie). Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
