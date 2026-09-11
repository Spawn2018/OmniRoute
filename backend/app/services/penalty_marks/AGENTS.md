# BC penalty_mark (CI5)

HITL katalog rodzaju naruszenia kary per tenant. mark_code + breach_kind otif|delay|damage|other + source_ref. Nie kara SQL. Nie auto linia.

## Dozwolone zależności
- `app.models.penalty_mark`
- `app.repositories.penalty_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sla_clauses, extraction, spend_marks)
- zapis `charge` / `sla_clause` / `spend_mark`
- kara SQL / amount / penalty / float / kwota
- HTTP
- UPDATE / DELETE wiersza
