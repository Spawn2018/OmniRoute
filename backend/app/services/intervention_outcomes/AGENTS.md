# BC intervention_outcome (CI7)

HITL katalog wyniku interwencji per tenant. outcome_code + result_kind contained|rerouted|claimed|other + source_ref. Nie SQL saved. Nie kwota.

## Dozwolone zależności
- `app.models.intervention_outcome`
- `app.repositories.intervention_outcomes`
- `app.domain`

## Zakaz
- import innych BC services (charges, remediation_options, repair_playbooks, extraction)
- zapis `charge` / `remediation_option` / `repair_playbook`
- predicted_loss / repair_cost / actual_loss / saved / amount / float / kwota
- HTTP
- UPDATE / DELETE wiersza
