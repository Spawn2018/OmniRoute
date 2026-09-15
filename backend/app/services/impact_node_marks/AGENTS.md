# BC impact_node_mark (AI6.0)

HITL katalog węzła kaskady skutku per tenant. mark_code + node_kind
shipment|inventory|sku|line|order|revenue|margin|cash|other + source_ref.
Nie SQL grafu. Nie EBITDA.

## Dozwolone zależności
- `app.models.impact_node_mark`
- `app.repositories.impact_node_marks`
- `app.domain`

## Zakaz
- import innych BC services (tower_impacts, impact_scenarios, line_impact_marks, charges, extraction)
- zapis `tower_impact` / `impact_scenario` / `line_impact_mark` / `charge` / `extraction_draft`
- SQL grafu / EBITDA / Watch Tower silnik / live plant
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
