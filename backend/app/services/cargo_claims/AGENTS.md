# BC cargo_claim (M-55)

Reklamacja ładunku per tenant, FK do `shipment`. HITL OS&D + terminy CMR + evidence bool jako dane. Nie kwota, nie scoring, nie ubezpieczenie, nie timedelta, nie live GPS.

## Dozwolone zależności
- `app.models.cargo_claim`
- `app.repositories.cargo_claims`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, charges)
- zapis `shipment` / `quotation` / `charge`
- kwoty / marża / float / scoring osoby
- timedelta 7/21/365
- live GPS / bajty zdjęcia
- HTTP
- UPDATE / DELETE wiersza
