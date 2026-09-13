# BC outcome_ledger (AI1.1)

HITL ledger faktu per tenant. target_bc + entity_id + suggestion_id + actual_value
Decimal + source_ref. Nie CRPS liczone. Nie FK do suggestion_ledger.

## Dozwolone zależności
- `app.models.outcome_ledger`
- `app.repositories.outcome_ledgers`
- `app.domain`

## Zakaz
- import innych BC services (suggestion_ledgers, prediction_ledgers, charges, extraction)
- zapis `suggestion_ledger` / `prediction_ledger` / `charge` / `extraction_draft`
- CRPS SQL / MAE SQL / Brier / champion
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do suggestion_ledger / shipment / trip
