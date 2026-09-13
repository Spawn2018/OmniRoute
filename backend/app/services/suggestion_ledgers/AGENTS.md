# BC suggestion_ledger (AI1.0)

HITL ledger podpowiedzi per tenant. target_bc + entity_id + przedział Decimal
+ reaction + changed_to + source_ref. Nie zapis LLM. Nie CRPS liczone.

## Dozwolone zależności
- `app.models.suggestion_ledger`
- `app.repositories.suggestion_ledgers`
- `app.domain`

## Zakaz
- import innych BC services (prediction_ledgers, operator_decisions, charges, extraction)
- zapis `prediction_ledger` / `operator_decision` / `charge` / `extraction_draft`
- zapis z modelu na L0–2 / CRPS SQL / champion
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do shipment / trip / quotation
