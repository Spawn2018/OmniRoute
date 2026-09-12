# BC fair_share_mark (EXP3.4)

HITL katalog znacznika fair share per tenant. mark_code + share_kind
fair|split|pool|other + source_ref. Nie allocation SQL. Nie druga marza.

## Dozwolone zaleznosci
- `app.models.fair_share_mark`
- `app.repositories.fair_share_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, cost_allocation_marks, extraction)
- zapis `charge` / `cost_allocation_mark`
- allocation SQL · qty float · druga marza
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
