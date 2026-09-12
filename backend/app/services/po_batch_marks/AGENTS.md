# BC po_batch_mark (EXP3.0d)

HITL katalog znacznika batch/lot na linii PO per tenant. mark_code + batch_kind
batch|lot|serial|other + source_ref. Nie live EDI. Nie auto shipment.

## Dozwolone zależności
- `app.models.po_batch_mark`
- `app.repositories.po_batch_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, asns, charges, extraction, po_plant_marks, po_sku_marks)
- zapis `purchase_order` / `po_line` / `asn` / `charge` / `extraction_draft`
- live EDI / auto shipment / qty / kwota
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `purchase_order` / `po_line`
