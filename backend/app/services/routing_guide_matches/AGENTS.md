# BC routing_guide_match (CT4 leftover)

HITL katalog trybu dopasowania przewodnika per tenant. mark_code + match_kind + source_ref. Nie silnik matching.

## Dozwolone zależności
- `app.models.routing_guide_match`
- `app.repositories.routing_guide_matches`
- `app.domain`

## Zakaz
- import innych BC services (routing_guides, shipments, asns, charges)
- zapis `shipment` / `asn` / `routing_guide`
- silnik matching lane/mode / float / kwota
- HTTP
- UPDATE / DELETE wiersza
