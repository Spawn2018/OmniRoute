# BC shipment_leg (M-48 / M-49 / M-50 / M-51)

Odcinek na zleceniu per tenant. 108.0 `road`, 109.0 `rail`, 110.0 `china_rail`, 111.0 `ocean_lcl`, 154.0 `air`, 209.0 HAWB/MAWB, 619.0 nadanie z prefiksu M-03, 622.0 cyfra IATA na wklejonym MAWB.
Nie mapa, nie GPS, nie TMS, nie kwota, nie korytarz, nie CFS, nie live IATA.

## Dozwolone zależności
- `app.models.shipment_leg`
- `app.repositories.shipment_legs`
- `app.domain`

## Zakaz
- import innych BC services (shipments, geography, charges, ocean_bills)
- zapis `shipment` / `location` / `port` / `charge` / `ocean_bill`
- kwoty / marża / float / ETA / live IATA / cyfra na HAWB i na puli
- import `organization_settings` (prefiks składa API)
- HTTP / leaflet
