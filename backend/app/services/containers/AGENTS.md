# BC container (T3)

Kontener ISO 6346 per tenant. Opcjonalne `shipment_id`. HITL VGM. HITL `booking_no`. HITL `carrier_party_id` (FK, bind w API). Nie S21.

## Dozwolone zależności
- `app.models.container`
- `app.repositories.containers`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, geography, trips)
- zapis `shipment` / `charge` / `terminal` / `party`
- kwoty / marża / float / TEU
- HTTP / PIN / mapa / kalkulator VGM / S21
