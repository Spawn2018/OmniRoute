# BC container (T3)

Kontener ISO 6346 per tenant. Opcjonalne `shipment_id`. HITL VGM. HITL `booking_no`. HITL `pin_code` (tekst). HITL `payload_kg` (Decimal, nie kalkulator). HITL `teu` (Decimal, nie kalkulator z typu ISO). HITL `carrier_party_id` (FK, bind w API). HITL `shipment_leg_id` (FK, bind w API). Nie S21.

## Dozwolone zależności
- `app.models.container`
- `app.repositories.containers`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, geography, trips)
- zapis `shipment` / `charge` / `terminal` / `party`
- kwoty / marża / float / TEU
- HTTP / live terminal PIN / ciphertext / mapa / kalkulator VGM / S21
