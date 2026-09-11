# BC routing_guide (CT4)

HITL katalog przewodnika routingu per tenant. guide_code + etykiety. Nie 409. Nie mapa.

## Dozwolone zależności
- `app.models.routing_guide`
- `app.repositories.routing_guides`
- `app.domain`

## Zakaz
- import innych BC services (shipments, trips, charges, extraction)
- zapis `shipment` / `trip` / `charge` / `asn`
- egzekucja 409 / auto stop / kwota / marża / float
- HTTP / mapa
- UPDATE / DELETE wiersza
- FK do `shipment` / geography
