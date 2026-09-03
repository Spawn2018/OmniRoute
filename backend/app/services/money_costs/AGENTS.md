# BC money_cost (M-43)

Koszt pieniądza per tenant. Wiąże `bank_payment` z `nbp_rate`.
Nie kwota, nie odsetki, nie mnożenie kursem.

## Dozwolone zależności
- `app.models.money_cost`
- `app.repositories.money_costs`
- `app.domain`

## Zakaz
- import innych BC services (bank_payments, nbp_rates, charges)
- zapis `bank_payment` / `nbp_rate` / `charge`
- kwoty / marża / float / mnożenie
- HTTP
