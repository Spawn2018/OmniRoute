# BC cash_discount (F2)

HITL rodzaj skonta per tenant, FK do `sales_invoice`. Nie kwota. Nie CAMT. Nie druga marża.

## Dozwolone zależności
- `app.models.cash_discount`
- `app.repositories.cash_discounts`
- `app.domain`

## Zakaz
- import innych BC services (sales_invoices, bank_payments, charges, quotations)
- zapis `sales_invoice` / `bank_payment` / `charge`
- kwoty / marża / float / Decimal / CAMT / period lock
- HTTP
