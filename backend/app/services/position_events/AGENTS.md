# BC position_event (BR2.0)

HITL katalog zdarzenia pozycji per tenant. event_code + source_kind
gps|manual|other + source_ref. Nie live GPS. Nie tracking_event.

## Dozwolone zależności
- `app.models.position_event`
- `app.repositories.position_events`
- `app.domain`

## Zakaz
- import innych BC services (tracking_events, telematics_connectors, trips, charges, extraction)
- zapis `tracking_event` / `telematics_connector` / `trip` / `resource` / `charge`
- live GPS / poll / mapa / wspolrzedne / float
- kwota / marża
- HTTP
- UPDATE / DELETE wiersza
- FK do `tracking_event` / `resource` / `trip`
