# BC time_to_fix_mark (EXP2.9)

HITL katalog znacznika TIME-TO-FIX per tenant. mark_code + fix_kind
open|wip|done|other + source_ref. Nie silnik TTF. Nie SLA SQL.

## Dozwolone zależności
- `app.models.time_to_fix_mark`
- `app.repositories.time_to_fix_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sla_clauses, extraction)
- zapis `charge` / `sla_clause` / `extraction_draft`
- live TIME-TO-FIX engine / SLA SQL / countdown
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
