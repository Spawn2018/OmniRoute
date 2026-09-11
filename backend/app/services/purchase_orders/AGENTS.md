# BC purchase_order (CT1)

HITL katalog nagłówka, linii i awiza zamówienia zakupu per tenant. po_code + po_line + asn. Nie live EDI. Nie auto shipment.

## Dozwolone zależności
- `app.models.purchase_order`
- `app.models.po_line`
- `app.models.asn`
- `app.repositories.purchase_orders`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, field_carry_forwards, edi_messages, extraction)
- zapis `shipment` / `charge` / `field_carry_forward` / `edi_message` / `extraction_draft`
- live EDI 856 / scrape / auto shipment
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipment` / `party` / geography
