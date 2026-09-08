# BC dock_appointment (D3)

Awizacja doku per tenant na `stop` magazynu spedycyjnego.
Nie WMS. Nie T8. Nie yard.

## Dozwolone zależności
- `app.models.dock_appointment`
- `app.repositories.dock_appointments`
- `app.domain`

## Zakaz
- import innych BC services (shipments, stops, geography, charges)
- zapis `shipment` / `stop` / `location` / `charge`
- kwoty / marża / float / slot optimizer
- HTTP / WMS
