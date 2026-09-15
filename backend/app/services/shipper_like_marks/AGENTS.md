# BC shipper_like_mark (BR6.2 leftover)

HITL katalog stance like-for-like per tenant. mark_code + like_kind
match|gap|bench|other + source_ref. Nie SQL. Nie Alpega.
Nie shipper_round_mark.

## Dozwolone zaleznosci
- `app.models.shipper_like_mark`
- `app.repositories.shipper_like_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipper_round_marks, shipper_tender_marks, tenders, charges, extraction)
- zapis `shipper_round_mark` / `shipper_tender_mark` / `tender` / `charge`
- auto-award / Alpega live / Freight Bench HTTP / like-for-like SQL / scoring
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `shipper_round_mark` / `shipper_tender_mark` / `tender` / `party`
