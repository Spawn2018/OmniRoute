# BC po_plant_mark (EXP3.0b)

HITL katalog znacznika plant/batch/SKU na PO per tenant. mark_code + plant_kind
plant|batch|sku|other + source_ref. Nie live EDI. Nie auto shipment.

## Dozwolone zależności
- `app.models.po_plant_mark`
- `app.repositories.po_plant_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, asns, charges, extraction)
- zapis `purchase_order` / `po_line` / `asn` / `charge` / `extraction_draft`
- live EDI / auto shipment / qty / kwota
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `purchase_order`
