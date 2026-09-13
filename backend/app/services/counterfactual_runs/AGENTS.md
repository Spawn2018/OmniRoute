# BC counterfactual_run (AI1.2 / AI4.1)

HITL katalog przebiegu what-if per tenant. run_code + plan_snapshot_id +
baseline_label + levers_label + result_label + source_ref.
Widok `what_if_replay` = ten sam SELECT, nie liczenie.
Nie solver liczb. Nie benefit_ledger.

## Dozwolone zależności
- `app.models.counterfactual_run`
- `app.models.what_if_replay`
- `app.repositories.counterfactual_runs`
- `app.domain`

## Zakaz
- import innych BC services (what_if_marks, plan_snapshots, circle_sims, charges, extraction)
- zapis `what_if_mark` / `plan_snapshot` / `circle_sim` / `charge` / `extraction_draft`
- solver what-if / JSON dźwigni / mnożenie
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- CASCADE
- FK proste tylko do `plan_snapshot.id` (musi być złożone z `organization_id`)
