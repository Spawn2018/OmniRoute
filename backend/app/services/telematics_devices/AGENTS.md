# BC telematics_device (BR2.1)

HITL katalog urzadzenia telematycznego per tenant. device_code + device_kind
tracker|fault|other + source_ref. Nie live poll. Nie parowanie z resource.

## Dozwolone zaleznosci
- `app.models.telematics_device`
- `app.repositories.telematics_devices`
- `app.domain`

## Zakaz
- import innych BC services (telematics_connectors, position_events, resources, trips, charges, extraction)
- zapis `telematics_connector` / `position_event` / `resource` / `trip` / `charge`
- live GPS / poll / mapa / parowanie SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `resource` / `trip` / `telematics_connector` / `position_event`
