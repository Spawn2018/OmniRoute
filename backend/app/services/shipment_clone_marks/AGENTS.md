# BC shipment_clone_mark (N9)

HITL katalog intencji klonu zlecenia per tenant. mark_code + clone_kind
last_similar|manual_pick|other + source_ref. Nie drugi SoR. Nie auto-copy.

## Dozwolone zależności
- `app.models.shipment_clone_mark`
- `app.repositories.shipment_clone_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, field_carry_forwards, charges, extraction)
- zapis `shipment` / `field_carry_forward` / `charge` / `extraction_draft`
- auto-copy / matching similar SQL / drugi SoR
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipment`
