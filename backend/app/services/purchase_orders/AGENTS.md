# BC purchase_order (CT1)

HITL katalog nagłówka i linii zamówienia zakupu per tenant. po_code + po_line (sku, qty Decimal, uom, etykiety). Nie ASN. Nie shipment.

## Dozwolone zależności
- `app.models.purchase_order`
- `app.models.po_line`
- `app.repositories.purchase_orders`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, field_carry_forwards, extraction)
- zapis `shipment` / `charge` / `field_carry_forward` / `extraction_draft`
- ASN / EDI 856 / auto shipment
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipment` / `party` / geography
