# BC routing_guide_enforcement (CT4 leftover)

HITL katalog trybu egzekucji przewodnika per tenant. mark_code + enforcement_kind + source_ref. Nie HTTP 409 na shipment.

## Dozwolone zależności
- `app.models.routing_guide_enforcement`
- `app.repositories.routing_guide_enforcements`
- `app.domain`

## Zakaz
- import innych BC services (routing_guides, shipments, asns, charges)
- zapis `shipment` / `asn` / `routing_guide`
- HTTP 409 na POST shipment/ASN / float / kwota
- HTTP
- UPDATE / DELETE wiersza
