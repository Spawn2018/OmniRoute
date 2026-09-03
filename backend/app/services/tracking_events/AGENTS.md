# BC tracking_event (M-36)

Zdarzenie śledzenia per tenant, FK do `shipment`. Nie mapa, nie czas przybycia, nie AIS.

## Dozwolone zależności
- `app.models.tracking_event`
- `app.repositories.tracking_events`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, geography)
- zapis `shipment` / `quotation` / `charge`
- kwoty / marża / float / czas przybycia liczony
- HTTP / mapa
