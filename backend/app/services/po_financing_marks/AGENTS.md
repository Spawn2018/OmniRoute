# BC po_financing_mark (BR5.1)

HITL katalog stance PO Financing per tenant. mark_code + financing_kind
po|release|advance|other + source_ref. Nie FK purchase_order. Nie wycena zapasu.

## Dozwolone zależności
- `app.models.po_financing_mark`
- `app.repositories.po_financing_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, factoring_connectors, inventory_position_marks, charges, extraction)
- zapis `purchase_order` / `po_line` / `asn` / `factoring_connector` / `charge`
- wycena zapasu SQL / wiekowanie BR1.2 / live partner HTTP / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
