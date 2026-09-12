# BC diversion_mark (EXP1)

HITL katalog znacznika diversion per tenant. mark_code + stance_kind
diversion|reroute|other + source_ref. Nie FK shipment. Nie cargo_value.

## Dozwolone zależności
- `app.models.diversion_mark`
- `app.repositories.diversion_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges, extraction)
- zapis `shipment` / `party` / `charge` / `extraction_draft`
- FK diversion_of_shipment_id / cargo_value / mapa / auto-reroute
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
