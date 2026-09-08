# BC resource (T2 / S50)

Katalog floty per tenant: pojazd / kierowca / naczepa. Nie trip. Nie HW.

## Dozwolone zależności
- `app.models.resource`
- `app.repositories.resources`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges, stops)
- zapis `shipment` / `party` / `trip` / `charge`
- kwoty / marża / float / km
- HTTP / mapa / `/fleet`
