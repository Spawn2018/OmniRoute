# BC purchase_order (CT1)

HITL katalog nagłówka zamówienia zakupu per tenant. po_code + opcjonalny plant_label + source_ref. Nie linia SKU. Nie ASN. Nie shipment.

## Dozwolone zależności
- `app.models.purchase_order`
- `app.repositories.purchase_orders`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, field_carry_forwards, extraction)
- zapis `shipment` / `charge` / `field_carry_forward` / `extraction_draft`
- `po_line` / SKU / qty / ASN / EDI 856 / auto shipment
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipment` / `party` / geography
