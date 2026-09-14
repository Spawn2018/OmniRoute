# BC line_impact_layer_mark (BR7.1)

HITL katalog warstwy liczonej wpływu na linię per tenant. mark_code +
layer_kind scored|forecast|actual|other + source_ref. Nie SQL. Nie EBITDA.

## Dozwolone zależności
- `app.models.line_impact_layer_mark`
- `app.repositories.line_impact_layer_marks`
- `app.domain`

## Zakaz
- import innych BC services (line_impact_marks, charges, extraction, demand_snapshot_marks)
- zapis `line_impact_mark` / `charge` / `extraction_draft`
- SQL line impact · EBITDA · plant live feed
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
