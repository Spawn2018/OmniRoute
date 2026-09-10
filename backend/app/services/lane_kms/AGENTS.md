# BC lane_km (G2.21)

HITL katalog km ładowny/pusty/dolot per tenant. km_code + trzy Decimal + source_ref. Nie Haversine. Nie trip.

## Dozwolone zależności
- `app.models.lane_km`
- `app.repositories.lane_kms`
- `app.domain`

## Zakaz
- import innych BC services (trips, shipments, resources, charges, geography, circle_sims, tenders)
- zapis `trip` / `shipment` / `charge` / `circle_sim` / `lane_pattern`
- Haversine / GPS / mapa / suma circle_sim / kwota / marża / float
- HTTP / LLM / silnik 500k / myto
- UPDATE / DELETE wiersza
