# BC cash_flow (M-45)

Przepływ per tenant. Wiąże `quotation` z `bank_payment`.
Nie kwota, nie odejmowanie, nie live HTTP.

## Dozwolone zależności
- `app.models.cash_flow`
- `app.repositories.cash_flows`
- `app.domain`

## Zakaz
- import innych BC services (quotations, bank_payments, charges)
- zapis `quotation` / `bank_payment` / `charge`
- kwoty / marża / float / odejmowanie
- HTTP
