# BC impact_edge_mark (AI6.0 leftover)

HITL katalog krawędzi kaskady skutku per tenant. mark_code + from_kind + to_kind
shipment|inventory|sku|line|order|revenue|margin|cash|other + source_ref.
Nie FK do impact_node_mark. Nie SQL grafu. Nie EBITDA.

## Dozwolone zależności
- `app.models.impact_edge_mark`
- `app.repositories.impact_edge_marks`
- `app.domain`

## Zakaz
- import innych BC services (impact_node_marks, tower_impacts, impact_scenarios, charges, extraction)
- zapis `impact_node_mark` / `tower_impact` / `impact_scenario` / `charge` / `extraction_draft`
- FK do `impact_node_mark` / SQL grafu / EBITDA / Watch Tower silnik / live plant
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
