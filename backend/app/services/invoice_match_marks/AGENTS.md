# BC invoice_match_mark (F10 leftover)

HITL katalog stancji dopasowania FV zakupu per tenant. mark_code +
match_kind candidate|rank|allocate|other + source_ref. Nie ranking SQL.
Nie allocation.

## Dozwolone zależności
- `app.models.invoice_match_mark`
- `app.repositories.invoice_match_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_invoices, charges, sales_invoices, extraction)
- zapis `purchase_invoice` / `charge` / `sales_invoice` / `extraction_draft`
- ranking SQL / score / auto-link / `invoice_match_candidate`
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
