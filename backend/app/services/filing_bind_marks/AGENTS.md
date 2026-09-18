# BC filing_bind_mark (C1 leftover)

HITL katalog stancji wiązania zgłoszenia per tenant. mark_code + bind_kind
shipment|scheme|both|other + source_ref. Nie FK shipment. Nie PUESC.

## Dozwolone zależności
- `app.models.filing_bind_mark`
- `app.repositories.filing_bind_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipment_monitoring_filings, monitoring_schemes, shipments, charges)
- zapis `shipment_monitoring_filing` / `monitoring_scheme` / `shipment` / `charge`
- FK shipment/scheme · PUESC · SENT XML
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
