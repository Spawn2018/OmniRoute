# BC shipper_round_mark (BR6.2 leftover)

HITL katalog rundy przetargu zaladowcy per tenant. mark_code + round_kind
first|second|final|other + source_ref. Nie tender_round. Nie Alpega.
Nie like-for-like SQL. Nie shipper_tender_mark.

## Dozwolone zaleznosci
- `app.models.shipper_round_mark`
- `app.repositories.shipper_round_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipper_tender_marks, tenders, tender_rounds, charges, extraction)
- zapis `shipper_tender_mark` / `tender` / `tender_round` / `charge`
- auto-award / Alpega live / Freight Bench HTTP / like-for-like SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipper_tender_mark` / `tender` / `tender_round` / `party`
