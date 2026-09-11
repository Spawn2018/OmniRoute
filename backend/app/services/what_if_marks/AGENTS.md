# BC what_if_mark (EXP2.10)

HITL katalog znacznika what-if per tenant. mark_code + scenario_kind
fuel|port|bankruptcy|other + source_ref. Nie silnik what-if. Nie plan_snapshot.

## Dozwolone zależności
- `app.models.what_if_mark`
- `app.repositories.what_if_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, plan_snapshots, extraction, trips)
- zapis `charge` / `plan_snapshot` / `extraction_draft`
- what-if silnik / paliwo SQL / port SQL / bankructwo SQL
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
