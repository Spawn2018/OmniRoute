# Rejestr modułów (skrót)

Pełny rejestr, plastry i zależności:  
`Informacje z claude/REJESTR-MODULOW-I-PLAN-v2.md` — **nie dumpować** do kontekstu.

Numeracja plastrów w kodzie: **0.3 = RLS**, **0.4 = OpenFGA** (nie outbox), **0.5 = Frontend Shell** (nie konfiguracja).

## Fundament i AI (to, co istnieje w kodzie)

| ID | Moduł | Plaster | Status |
|---|---|---|---|
| M-01 | Wielodostępność / tenancy | 0.3 RLS + 0.4 OpenFGA + 0.12 JWT + 0.15 hasła | **ukończony (fundament)** · Auth0 I1 po Wave A |
| M-20 | Ekstrakcja dokumentów | 0.7–0.14 HITL/instructor/docling/langfuse/XOR/split/HTTP unit | **ukończony (fundament)** (HTTP = unit stub, nie live PG) |
| M-02 | Outbox / idempotencja | nie 0.4 | planowany |
| M-03 | Konfiguracja jako dane | nie 0.5 | planowany |
| M-06 | charge_code + aliasy | 1.0 katalog | **ukończony (fundament)** · aliasy na wierszu; nie `rate_line` / `charge` |
| M-21 | Silnik wyceny (SQL) | 2.x | planowany |

Nie dopisuj tu 70 pustych wierszy M-xx. Reszta rejestru zostaje w archiwum Claude.

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony (fundament)** — gate green + wzorzec do kopiowania; nie oznacza całego produktu
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł w kodzie: `docs/spec/<nazwa>.md` (max 400 linii).  
Dziś: `tenancy.md`, `extraction.md`, `charge-code.md`. Szkielety uzupełniane przy plastrze — nie kompiluj całego archiwum.
