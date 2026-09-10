# BC container (T3)

Kontener ISO 6346 per tenant. Opcjonalne `shipment_id`. HITL VGM (`vgm_kg` / `vgm_method` / `vgm_cutoff_at`). Nie booking.

## Dozwolone zależności
- `app.models.container`
- `app.repositories.containers`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, geography, trips)
- zapis `shipment` / `charge` / `terminal` / `party`
- kwoty / marża / float / TEU
- HTTP / PIN / mapa / kalkulator VGM
