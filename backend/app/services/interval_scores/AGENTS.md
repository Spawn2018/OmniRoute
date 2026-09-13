# BC interval_score (AI2.0)

Widok MAE + CRPS jednostajnego ze złączenia suggestion_ledger × outcome_ledger.
Postgres liczy. Nie wpis. Nie prediction_ledger.

## Dozwolone zależności
- `app.models.interval_score`
- `app.repositories.interval_scores`
- `app.domain`

## Zakaz
- import innych BC services (suggestion_ledgers, outcome_ledgers, prediction_ledgers, charges, extraction)
- zapis `suggestion_ledger` / `outcome_ledger` / `prediction_ledger` / `charge`
- liczenie CRPS/MAE w Pythonie
- Brier / champion / dryf
- kwota / marża / float
- HTTP
- INSERT / UPDATE / DELETE widoku
