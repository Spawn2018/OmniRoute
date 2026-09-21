# BC container (T3)

Kontener ISO 6346 per tenant. Opcjonalne `shipment_id`. HITL VGM. HITL `booking_no`. HITL `pin_code` (tekst). HITL `grade` (tekst, nie IICL live). HITL `vessel_imo` (tekst, nie AIS). HITL `alliance_service` (tekst, nie live alliance). HITL `pol_unlocode` (tekst UN/LOCODE, nie FK portu, nie mapa). HITL `payload_kg` (Decimal, nie kalkulator). HITL `teu` (Decimal, nie kalkulator z typu ISO). HITL `quantity` (Integer, nie stop). HITL `weight_kg` (Decimal, nie stop, nie VGM). HITL `volume_m3` (Decimal, nie kalkulator CBM). HITL `pickup_date` (date, nie countdown). HITL `return_date` (date, nie countdown). HITL `gate_in_date` (date, nie countdown). HITL `delivery_date` (date, nie countdown). HITL `unload_date` (date, nie countdown). HITL `temp_min` (Decimal °C, nie float). HITL `temp_max` (Decimal °C, nie float; band + 409 bez reefer). HITL `needs_external_power` (bool; 409 bez reefer, nie N3). HITL `carrier_party_id` (FK, bind w API). HITL `container_release_party_id` (FK, bind w API). HITL `shipment_leg_id` (FK, bind w API). Nie S21.

## Dozwolone zależności
- `app.models.container`
- `app.repositories.containers`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, geography, trips)
- zapis `shipment` / `charge` / `terminal` / `party`
- kwoty / marża / float / TEU
- HTTP / live terminal PIN / ciphertext / mapa / kalkulator VGM / S21
