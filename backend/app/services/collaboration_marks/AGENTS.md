# BC collaboration_mark (CT11)

HITL katalog roli współpracy per tenant. mark_code + role_kind + source_ref. Nie wspólny SELECT. Nie tuple OpenFGA per strona.

## Dozwolone zależności
- `app.models.collaboration_mark`
- `app.repositories.collaboration_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, shipment_stakeholders, charges)
- zapis `shipment` / `party` / `shipment_stakeholder`
- wspólny SELECT cross-shipper / tuple OpenFGA per strona / float / kwota
- HTTP
- UPDATE / DELETE wiersza
