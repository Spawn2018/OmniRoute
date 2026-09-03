# BC quote_invoice_settlement (M-41)

Rozliczenie wyceny z fakturą per tenant. Wiąże `quotation` z `sales_invoice`.
Nie kwota, nie druga marża, nie live HTTP.

## Dozwolone zależności
- `app.models.quote_invoice_settlement`
- `app.repositories.quote_invoice_settlements`
- `app.domain`

## Zakaz
- import innych BC services (quotations, sales_invoices, charges)
- zapis `quotation` / `sales_invoice` / `charge`
- kwoty / marża / float
- HTTP
