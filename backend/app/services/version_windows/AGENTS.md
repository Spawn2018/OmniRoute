# BC version_window (AI2.1 leftover)

Widok średnich MAE/CRPS per model_version i dzień UTC. Postgres liczy.
Nie detektor. Nie auto-champion.

## Dozwolone zależności
- `app.models.version_window`
- `app.repositories.version_windows`
- `app.domain`

## Zakaz
- import innych BC services (version_scores, interval_scores, suggestion_ledgers, charges)
- zapis `version_score` / `interval_score` / `suggestion_ledger` / `charge`
- liczenie średnich w Pythonie
- próg dryfu / flaga detektora / auto-przełączenie modelu
- Brier
- kwota / marża / float
- HTTP
- INSERT / UPDATE / DELETE widoku
