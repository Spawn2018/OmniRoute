# BC fleet_cost_mark (EXP2.15)

HITL katalog znacznika kosztu floty per tenant. mark_code + cost_kind
tco|maintenance|lease|other + source_ref. Nie TCO SQL. Nie CMMS silnik.
Obok `cmms_mark` (G7) — tu koszt, nie work_order/DTC.

## Dozwolone zależności
- `app.models.fleet_cost_mark`
- `app.repositories.fleet_cost_marks`
- `app.domain`

## Zakaz
- import innych BC services (cmms_marks, resources, charges, extraction)
- zapis `cmms_mark` / `resource` / `charge` / `extraction_draft`
- fleet cost live / TCO SQL / work_order / kara kierowcy
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza