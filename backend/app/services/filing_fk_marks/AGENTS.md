# BC filing_fk_mark (C1 leftover)

HITL katalog celu FK zgłoszenia per tenant. mark_code + fk_kind
shipment|scheme|other + source_ref. Nie live FK. Nie PUESC.

## Dozwolone zależności
- `app.models.filing_fk_mark`
- `app.repositories.filing_fk_marks`
- `app.domain`

## Zakaz
- import innych BC services (filing_bind_marks, shipments, monitoring_schemes, charges)
- zapis `shipment` / `monitoring_scheme` / `shipment_monitoring_filing` / `charge`
- live FK UUID / PUESC / SENT XML
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
