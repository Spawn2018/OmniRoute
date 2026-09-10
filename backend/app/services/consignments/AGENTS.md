# BC consignment (N1)

HITL przesyłka per tenant, FK do `shipment`. N wierszy. Nie paczka. Nie FTL unique.

## Dozwolone zależności
- `app.models.consignment`
- `app.repositories.consignments`
- `app.domain`

## Zakaz
- import innych BC services (shipments, stops, shipment_packages, charges)
- zapis `shipment` / `stop` / `shipment_package` / `charge`
- unique FTL=1 / kwota / marża / float
- HTTP / mapa / WMS
