# BC stop_group (T1b)

HITL nagłówek grupy punktów per tenant, FK do `shipment`. N wierszy.
Kolumna `stop.stop_group_code` zostaje. Nie członkostwo FK.

## Dozwolone zależności
- `app.models.stop_group`
- `app.repositories.stop_groups`
- `app.domain`

## Zakaz
- import innych BC services (shipments, stops, consignments, charges)
- zapis `stop` / `shipment` / `charge`
- członkostwo / mapa / GPS / kwota / float
- HTTP
