# BC purchase_invoice (F10)

HITL katalog faktury zakupu per tenant. invoice_ref + invoice_kind
noted|other + source_ref. Nie ranking. Nie allocation. Nie kwota.

## Dozwolone zależności
- `app.models.purchase_invoice`
- `app.repositories.purchase_invoices`
- `app.domain`

## Zakaz
- import innych BC services (sales_invoices, charges, erp_connectors, extraction)
- zapis `sales_invoice` / `charge` / `erp_connector` / `extraction_draft`
- ranking SQL / auto-link / allocation / kwota / float
- HTTP
- UPDATE / DELETE wiersza
