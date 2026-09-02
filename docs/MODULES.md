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
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` · 5.1 POL/POD + `party_id` · 16.0 odczyt `nbp_rate` | **ukończony (fundament)** · nie marża; nie k6; nie override; nie mnożenie kwoty |
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

Nie dopisuj tu 70 pustych wierszy M-xx. Katalog + **kolejka Q1…** (co budować jedno po drugim, tryb Plan potem plaster): `docs/PLAN-REALIZACJA.md` § Kolejka. Archiwum Claude zostaje magazynem specyfikacji, nie SoT kolejności.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`, `rate-line.md`, `charge.md`, `quotation.md`, `organization-setting.md`, `geography.md` (4.0–4.2 w kodzie), `parties.md` (5.0 + 8.0 matcher maila w kodzie), `commodity-code.md` (5.2 w kodzie), `nbp-rate.md` (6.0 w kodzie), `dangerous-good.md` (7.0 w kodzie), `network.md` (9.0 w kodzie), `party-scorecard.md` (10.0 w kodzie), `customer-sop.md` (11.0 w kodzie), `port-surcharge.md` (12.0 w kodzie), `channel-quote.md` (13.0 w kodzie), `credit-review.md` (14.0 w kodzie), `finance-board.md` (15.0 w kodzie). Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
