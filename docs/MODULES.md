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
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` · 5.1 POL/POD + `party_id` | **ukończony (fundament)** · nie marża; nie k6; nie override |
| M-05 | Geografia | 4.0 `port` + 4.1 `location`/strefy + 4.2 `terminal`/WPI | **ukończony (fundament)** · `operator_party_id` od 5.0; `operator_name` zostaje |
| M-10 | Kontrahenci | 5.0 `party` + katalog zależny | **ukończony (fundament)** · lookup = szkic/fixture; override nie karmić wyceny |
| M-09 | Kody towarowe | 5.2 `commodity_code` | **ukończony (fundament)** · nie podpięcie do wyceny; nie IMDG |
| M-23 | Kurs NBP | 6.0 `nbp_rate` | **ukończony (fundament)** · nie przeliczenie wyceny; nie żywe M-07 `rate_line` |

Nie dopisuj tu 70 pustych wierszy M-xx. Katalog + **kolejka Q1…** (co budować jedno po drugim, tryb Plan potem plaster): `docs/PLAN-REALIZACJA.md` § Kolejka. Archiwum Claude zostaje magazynem specyfikacji, nie SoT kolejności.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`, `rate-line.md`, `charge.md`, `quotation.md`, `organization-setting.md`, `geography.md` (4.0–4.2 w kodzie), `parties.md` (5.0 w kodzie), `commodity-code.md` (5.2 w kodzie), `nbp-rate.md` (6.0 w kodzie). Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
