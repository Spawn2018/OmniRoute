# BC shipment_leg (M-48 / M-49 / M-50)

Odcinek na zleceniu per tenant. 108.0 `road`, 109.0 `rail`, 110.0 `china_rail`.
Nie mapa, nie GPS, nie TMS, nie kwota, nie korytarz.

## Dozwolone zależności
- `app.models.shipment_leg`
- `app.repositories.shipment_legs`
- `app.domain`

## Zakaz
- import innych BC services (shipments, geography, charges)
- zapis `shipment` / `location` / `port` / `charge`
- kwoty / marża / float / ETA
- HTTP / leaflet
