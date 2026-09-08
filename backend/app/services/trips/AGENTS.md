# BC trip (T2b / S50)

Przejazd per tenant: numer + status + opcjonalna flota. Nie km. Nie mapa.

## Dozwolone zależności
- `app.models.trip`
- `app.repositories.trips`
- `app.domain`

## Zakaz
- import innych BC services (resources, shipments, charges, stops)
- zapis `resource` / `shipment` / `stop` / `charge`
- kwoty / marża / float / km
- HTTP / mapa / `/fleet`
