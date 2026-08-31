# Rejestr modułów M-01…M-71 (skrót)

Pełny rejestr, plastry i zależności:  
`Informacje z claude/REJESTR-MODULOW-I-PLAN-v2.md`

## Faza 0 — fundament (start)

| ID | Moduł | Plaster startowy | Status |
|---|---|---|---|
| M-01 | Wielodostępność / tenancy | 0.3 RLS + test izolacji | **następny** |
| M-02 | Outbox / idempotencja | 0.4 | planowany |
| M-03 | Konfiguracja jako dane | 0.5 | planowany |
| M-06 | charge_code + aliasy | 1.x | planowany |
| M-21 | Silnik wyceny (SQL) | 2.x | planowany |

## Legenda statusów

- **planowany** — spec w `docs/spec/` do uzupełnienia przed kodem
- **w toku** — wpis w CURRENT.md
- **ukończony** — gate green + spec scalona

## Specyfikacje

Każdy moduł: `docs/spec/<nazwa>.md` (max 400 linii).  
Na start tylko szkielety — kompilacja z aneksów w Fazie B.
