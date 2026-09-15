# BC shipper_bind_mark (BR6.2 leftover)

HITL katalog stance wiązania załadowcy per tenant. mark_code + bind_kind
tender|party|other + source_ref. Nie Alpega live. Nie FK UUID.

## Dozwolone zależności
- `app.models.shipper_bind_mark`
- `app.repositories.shipper_bind_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipper_tender_marks, tenders, parties, charges, extraction)
- zapis `shipper_tender_mark` / `tender` / `party` / `charge`
- Alpega live / FK UUID / auto-award / scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `tender` / `shipper_tender_mark` / `party`
