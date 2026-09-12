# BC po_sku_mark (EXP3.0c)

HITL katalog znacznika SKU na linii PO per tenant. mark_code + sku_kind
sku|gtin|customer_sku|other + source_ref. Nie live EDI. Nie auto shipment.

## Dozwolone zależności
- `app.models.po_sku_mark`
- `app.repositories.po_sku_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, asns, charges, extraction, po_plant_marks)
- zapis `purchase_order` / `po_line` / `asn` / `charge` / `extraction_draft`
- live EDI / auto shipment / qty / kwota
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `purchase_order` / `po_line`
