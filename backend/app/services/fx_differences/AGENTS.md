# BC fx_difference (M-44)

Różnica kursowa per tenant. Wiąże `quotation` z `nbp_rate`.
Nie kwota, nie przeliczenie, nie live HTTP.

## Dozwolone zależności
- `app.models.fx_difference`
- `app.repositories.fx_differences`
- `app.domain`

## Zakaz
- import innych BC services (quotations, nbp_rates, charges)
- zapis `quotation` / `nbp_rate` / `charge`
- kwoty / marża / float / mnożenie
- HTTP
