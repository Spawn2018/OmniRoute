# BC inventory_position_mark (EXP3.3)

HITL katalog znacznika inventory position per tenant. mark_code + stock_kind
position|plant|sku|other + source_ref. Nie WMS live. Nie bilans SQL.

## Dozwolone zaleznosci
- `app.models.inventory_position_mark`
- `app.repositories.inventory_position_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, shipments, charges, extraction)
- zapis `po_line` / `shipment` / `charge`
- WMS live · bilans SQL · qty float
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
