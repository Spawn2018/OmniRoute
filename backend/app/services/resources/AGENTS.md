# BC resource (T2 / S50)

Katalog floty per tenant: pojazd / kierowca / naczepa. HITL `capacity_kg` / `capacity_ldm`
(Decimal). Nie trip. Nie HW. Nie m³ w tym BC (leftover).

## Dozwolone zależności
- `app.models.resource`
- `app.repositories.resources`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges, stops)
- zapis `shipment` / `party` / `trip` / `charge`
- kwoty / marża / float / km / Haversine
- HTTP / mapa / kalkulator LDM
- UPDATE / DELETE wiersza (zmiana = supersede)
