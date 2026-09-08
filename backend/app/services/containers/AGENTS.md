# BC container (T3)

Kontener ISO 6346 per tenant. Opcjonalne `shipment_id`. Nie VGM. Nie booking.

## Dozwolone zależności
- `app.models.container`
- `app.repositories.containers`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, geography, trips)
- zapis `shipment` / `charge` / `terminal` / `party`
- kwoty / marża / float / VGM / TEU
- HTTP / PIN / mapa
