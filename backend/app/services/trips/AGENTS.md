# BC trip (T2b / S50 / P5)

Przejazd per tenant: numer + status + opcjonalna flota + snapshot `expected_buy` + HITL `planned_distance_km` + HITL `actual_distance_km`. Nie liczenie km. Nie mapa. Nie wariancja.

## Dozwolone zależności
- `app.models.trip`
- `app.repositories.trips`
- `app.domain`

## Zakaz
- import innych BC services (resources, shipments, charges, stops)
- zapis `resource` / `shipment` / `stop` / `charge`
- marża / float / liczenie km / wariancja SQL na `charge`
- HTTP / mapa / `/fleet`
