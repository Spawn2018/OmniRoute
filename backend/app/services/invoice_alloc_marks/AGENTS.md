# BC invoice_alloc_mark (F10 leftover)

HITL katalog stancji alokacji FV zakupu per tenant. mark_code +
alloc_kind line|header|batch|other + source_ref. Nie allocation z kwotą.
Nie ranking SQL.

## Dozwolone zależności
- `app.models.invoice_alloc_mark`
- `app.repositories.invoice_alloc_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_invoices, invoice_match_marks, charges, extraction)
- zapis `purchase_invoice` / `invoice_match_mark` / `charge` / `extraction_draft`
- `purchase_invoice_allocation` / ranking SQL / score / auto-link
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
