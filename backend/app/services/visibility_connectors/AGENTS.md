# BC visibility_connector (CT7)

HITL katalog konektora widoczności per tenant. connector_code + system_kind `p44` + source_ref. Nie live HTTP. Nie sekrety. Nie AIS.

## Dozwolone zależności
- `app.models.visibility_connector`
- `app.repositories.visibility_connectors`
- `app.domain`

## Zakaz
- import innych BC services (charges, tracking_events, telematics_connectors, extraction)
- zapis `tracking_event` / `telematics_connector` / `charge` / `extraction_draft`
- live p44 / FourKites / Shippeo / scrape ocean / AIS
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / `api_key` / `base_url`
