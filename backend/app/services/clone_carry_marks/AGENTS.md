# BC clone_carry_mark (leftover 528 / N9)

HITL katalog stance carry U1 przy klonie per tenant. mark_code +
carry_kind carry|held|skip|other + source_ref. Nie auto-copy.
Nie similar SQL. Nie F2b.

## Dozwolone zależności
- `app.models.clone_carry_mark`
- `app.repositories.clone_carry_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipment_clone_marks, field_carry_forwards, shipments, charges, extraction)
- zapis `shipment_clone_mark` / `field_carry_forward` / `shipment` / `charge` / `extraction_draft`
- auto-copy allowlisty U1 / similar SQL / F2b Decimal
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipment` / `shipment_clone_mark` / `field_carry_forward`
