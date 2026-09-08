# BC shipment_package (D2)

Paczka na zleceniu per tenant. Skan QR Omni, `stop` z tej samej trasy.
Nie WMS. Nie auto-link bez prefiksu Omni.

## Dozwolone zależności
- `app.models.shipment_package`
- `app.repositories.shipment_packages`
- `app.domain`

## Zakaz
- import innych BC services (shipments, stops, geography, charges)
- zapis `shipment` / `stop` / `charge`
- kwoty / marża / float / kamera
- HTTP / WMS
