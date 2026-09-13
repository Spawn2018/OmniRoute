# BC counterfactual_run (AI1.2)

HITL katalog przebiegu what-if per tenant. run_code + baseline_label +
levers_label + result_label + source_ref. Nie silnik. Nie benefit_ledger.

## Dozwolone zależności
- `app.models.counterfactual_run`
- `app.repositories.counterfactual_runs`
- `app.domain`

## Zakaz
- import innych BC services (what_if_marks, plan_snapshots, circle_sims, charges, extraction)
- zapis `what_if_mark` / `plan_snapshot` / `circle_sim` / `charge` / `extraction_draft`
- silnik what-if / AI4.1 / JSON dźwigni
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do shipment / trip / plan_snapshot
