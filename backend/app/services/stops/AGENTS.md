# BC stop (T1)

Punkt operacyjny na zleceniu per tenant. Miejsce ze słownika. Dwa ETA HITL. Nie mapa, nie trip.

## Dozwolone zależności
- `app.models.stop`
- `app.repositories.stops`
- `app.domain`

## Zakaz
- import innych BC services (shipments, geography, charges)
- zapis `shipment` / `location` / `charge`
- kwoty / marża / float / ETA liczona z GPS lub pogody
- HTTP / leaflet
