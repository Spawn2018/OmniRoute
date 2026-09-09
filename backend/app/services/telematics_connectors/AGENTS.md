# BC telematics_connector (V5)

HITL katalog adaptera GPS per tenant. observation_kind + provider_code. Nie poll. Nie sekrety.

## Dozwolone zależności
- `app.models.telematics_connector`
- `app.repositories.telematics_connectors`
- `app.domain`

## Zakaz
- import innych BC services (resources, trips, charges, extraction)
- zapis `resource` / `trip` / `charge` / `tracking_event`
- lat/lng / poll / ciphertext / kwota / marża / float
- HTTP / GBOX / IKOL live
