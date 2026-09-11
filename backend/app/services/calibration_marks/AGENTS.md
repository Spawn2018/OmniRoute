# BC calibration_mark (CI7)

HITL katalog znacznika gotowości próbki per tenant. mark_code + sample_ready ready|pending + source_ref. Nie MAE SQL. Nie scoring.

## Dozwolone zależności
- `app.models.calibration_mark`
- `app.repositories.calibration_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, prediction_ledgers, party_scorecards, extraction)
- zapis `charge` / `prediction_ledger` / `party_scorecard`
- MAE SQL / float / kwota / marża
- HTTP
- UPDATE / DELETE wiersza
