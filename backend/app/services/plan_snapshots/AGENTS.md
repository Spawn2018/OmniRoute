# BC plan_snapshot (B0b)

HITL wersja planu per tenant. snapshot_code + trójka UUID z FK RESTRICT + autor + czas. Nie silnik. Nie kółka.
Q3 (2026-09-13): FK do shipment/trip/resource w AI4.0, `ON DELETE RESTRICT`. Nadal zakaz UPDATE/DELETE wiersza snapshot.

## Dozwolone zależności
- `app.models.plan_snapshot`
- `app.repositories.plan_snapshots`
- `app.domain`

## Zakaz
- import innych BC services (trips, shipments, resources, charges, extraction)
- zapis `trip` / `shipment` / `resource` / `charge`
- CASCADE na FK trójki
- circle_sim / what-if / km / kwota / marża / float
- HTTP / T8 live API / mapa
- UPDATE / DELETE wiersza
