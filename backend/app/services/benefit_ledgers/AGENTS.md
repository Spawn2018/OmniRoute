# BC benefit_ledger (AI1.3)

HITL ledger oszczędności per tenant. benefit_code + method_label +
hours_saved + saved_amount Decimal + saved_currency + source_ref.
Nie SQL z charge. Nie druga marża.

## Dozwolone zależności
- `app.models.benefit_ledger`
- `app.repositories.benefit_ledgers`
- `app.domain`

## Zakaz
- import innych BC services (charges, outcome_ledgers, counterfactual_runs, extraction)
- zapis `charge` / `outcome_ledger` / `counterfactual_run` / `extraction_draft`
- SQL vs charge / druga marża / liczenie oszczędności
- float
- HTTP
- UPDATE / DELETE wiersza
- FK do charge / outcome_ledger / counterfactual_run
