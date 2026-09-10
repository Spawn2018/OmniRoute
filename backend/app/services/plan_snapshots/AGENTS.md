# BC plan_snapshot (B0b)

HITL wersja planu per tenant. snapshot_code + trójka UUID jako dane + autor + czas. Nie silnik. Nie kółka.

## Dozwolone zależności
- `app.models.plan_snapshot`
- `app.repositories.plan_snapshots`
- `app.domain`

## Zakaz
- import innych BC services (trips, shipments, resources, charges, extraction)
- zapis `trip` / `shipment` / `resource` / `charge`
- FK do shipment/trip/resource
- circle_sim / what-if / km / kwota / marża / float
- HTTP / T8 live API / mapa
- UPDATE / DELETE wiersza
