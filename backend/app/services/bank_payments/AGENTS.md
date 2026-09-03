# BC bank_payment (M-42)

Płatność faktury na rachunek per tenant. Wiąże `sales_invoice` z `party_bank_account`.
Nie kwota, nie SEPA, nie live HTTP.

## Dozwolone zależności
- `app.models.bank_payment`
- `app.repositories.bank_payments`
- `app.domain`

## Zakaz
- import innych BC services (sales_invoices, parties, charges)
- zapis `sales_invoice` / `party_bank_account` / `charge`
- kwoty / marża / float
- HTTP
