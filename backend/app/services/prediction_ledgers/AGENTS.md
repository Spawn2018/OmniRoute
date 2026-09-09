# BC prediction_ledger (B0b / V1)

HITL ledger predykcji per tenant. Przedział N7 + CRPS/MAE jako dane. Nie silnik. Nie scoring osoby.

## Dozwolone zależności
- `app.models.prediction_ledger`
- `app.repositories.prediction_ledgers`
- `app.domain`

## Zakaz
- import innych BC services (trips, stops, charges, extraction)
- zapis `trip` / `stop` / `charge` / `plan_snapshot`
- liczenie CRPS/MAE / champion / drift / LLM
- kwota / marża / float
- HTTP / GPS / AIS / scoring osoby
- UPDATE / DELETE wiersza
