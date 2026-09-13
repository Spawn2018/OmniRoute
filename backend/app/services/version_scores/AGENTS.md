# BC version_score (AI2.1)

Widok średnich MAE/CRPS per model_version. Postgres liczy. Nie auto-champion.
Nie dryf.

## Dozwolone zależności
- `app.models.version_score`
- `app.repositories.version_scores`
- `app.domain`

## Zakaz
- import innych BC services (interval_scores, suggestion_ledgers, prediction_ledgers, charges)
- zapis `interval_score` / `suggestion_ledger` / `prediction_ledger` / `charge`
- liczenie średnich w Pythonie
- auto-przełączenie modelu / flaga champion
- dryf / Brier
- kwota / marża / float
- HTTP
- INSERT / UPDATE / DELETE widoku
