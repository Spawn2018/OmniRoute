# BC haulier_role_mark (EXP1)

HITL katalog roli przewoznika per tenant. mark_code + role_kind
booked|actual|other + source_ref. Nie FK party na shipment. Nie cargo_value.

## Dozwolone zależności
- `app.models.haulier_role_mark`
- `app.repositories.haulier_role_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges, extraction)
- zapis `shipment` / `party` / `charge` / `extraction_draft`
- FK booked/actual haulier na shipment / cargo_value / diversion
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
