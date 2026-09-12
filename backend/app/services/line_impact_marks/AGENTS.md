# BC line_impact_mark (EXP3.3b)

HITL katalog znacznika skutku linii per tenant. mark_code + impact_kind
line|plant|sku|other + source_ref. Nie SQL line impact. Nie EBITDA. Nie plant live.

## Dozwolone zależności
- `app.models.line_impact_mark`
- `app.repositories.line_impact_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, demand_snapshot_marks)
- zapis `charge` / `extraction_draft` / `demand_snapshot_mark`
- SQL line impact / EBITDA / plant live feed
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
