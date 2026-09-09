# BC monitoring_scheme (C7)

HITL katalog schematu monitoringu per tenant. scheme_code + source_ref. Nie zgłoszenie SENT. Nie PUESC. Nie marża.

## Dozwolone zależności
- `app.models.monitoring_scheme`
- `app.repositories.monitoring_schemes`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, extraction, geography)
- zapis `shipment` / `charge` / `party_document`
- SENT XML / PUESC HTTP / scrape / LLM / kwota / marża / float
- wymyślony klon SENT w kraju bez urzędu
