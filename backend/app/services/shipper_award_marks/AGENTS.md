# BC shipper_award_mark (BR6.2 leftover)

HITL katalog stance nagrody załadowcy per tenant. mark_code + award_kind
go|hold|no_award|other + source_ref. Nie Alpega live. Nie auto-award SQL.

## Dozwolone zależności
- `app.models.shipper_award_mark`
- `app.repositories.shipper_award_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipper_bind_marks, tenders, parties, charges, extraction)
- zapis `shipper_bind_mark` / `tender` / `tender_win_loss` / `charge`
- Alpega live / auto-award SQL / UPDATE tender.status / scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `tender` / `shipper_tender_mark` / `party`
