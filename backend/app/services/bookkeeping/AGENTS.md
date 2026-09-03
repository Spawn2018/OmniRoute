# BC bookkeeping (M-47)

Dekret per tenant. Wiąże `charge` z `sales_invoice`.
Nie kwota, nie JPK, nie ERP, nie live HTTP.

## Dozwolone zależności
- `app.models.bookkeeping`
- `app.repositories.bookkeeping`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices)
- zapis `charge` / `sales_invoice`
- kwoty / marża / float / odejmowanie
- HTTP
