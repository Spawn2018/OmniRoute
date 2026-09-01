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
| M-21 | Silnik wyceny (SQL) | 2.0 INSERT…SELECT z `rate_line` | **ukończony (fundament)** · nie marża; nie k6 |

Nie dopisuj tu 70 pustych wierszy M-xx. Katalog + **kolejka Q1…** (co budować jedno po drugim, tryb Plan potem plaster): `docs/PLAN-REALIZACJA.md` § Kolejka. Archiwum Claude zostaje magazynem specyfikacji, nie SoT kolejności.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`, `rate-line.md`, `charge.md`, `quotation.md`, `organization-setting.md`. Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
