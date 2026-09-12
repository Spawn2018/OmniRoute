# BC customer_po_mark (EXP1)

HITL katalog referencji PO klienta per tenant. mark_code + ref_kind
customer_po|release|call_off|other + source_ref. Nie purchase_order CT1. Nie kwota.

## Dozwolone zależności
- `app.models.customer_po_mark`
- `app.repositories.customer_po_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, shipments, charges, extraction)
- zapis `purchase_order` / `po_line` / `shipment` / `charge` / `extraction_draft`
- purchase_order CT1 / kolumna customer_po na shipment / EDI live
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
