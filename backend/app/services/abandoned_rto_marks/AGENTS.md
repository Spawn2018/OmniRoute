# BC abandoned_rto_mark (EXP3.10)

HITL katalog znacznika abandoned/RTO per tenant. mark_code + fate_kind
bl|loi|switch|other + source_ref. Nie abandoned live. Nie RTO scrape.

## Dozwolone zaleznosci
- `app.models.abandoned_rto_mark`
- `app.repositories.abandoned_rto_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, extraction)
- zapis `shipment` / `charge`
- abandoned live · RTO scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
