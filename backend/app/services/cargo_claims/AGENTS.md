# BC cargo_claim (M-55)

Reklamacja ładunku per tenant, FK do `shipment`. Nie kwota, nie scoring, nie ubezpieczenie.

## Dozwolone zależności
- `app.models.cargo_claim`
- `app.repositories.cargo_claims`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, charges)
- zapis `shipment` / `quotation` / `charge`
- kwoty / marża / float / scoring osoby
- HTTP
