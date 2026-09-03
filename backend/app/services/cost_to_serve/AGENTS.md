# BC cost_to_serve (M-46)

Koszt obsługi per tenant. Wiąże `customer_sop` z `quotation`.
Nie kwota, nie suma, nie ABC, nie live HTTP.

## Dozwolone zależności
- `app.models.cost_to_serve`
- `app.repositories.cost_to_serve`
- `app.domain`

## Zakaz
- import innych BC services (parties, quotations, charges)
- zapis `customer_sop` / `quotation` / `charge`
- kwoty / marża / float / suma
- HTTP
