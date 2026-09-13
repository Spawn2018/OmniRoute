# BC shipper_tender_mark (BR6.2)

HITL katalog trybu przetargu zaladowcy per tenant. mark_code + shipper_kind
round|bench|spot|other + source_ref. Nie druga tabela tender. Nie Alpega.

## Dozwolone zaleznosci
- `app.models.shipper_tender_mark`
- `app.repositories.shipper_tender_marks`
- `app.domain`

## Zakaz
- import innych BC services (tenders, tender_rounds, charges, extraction)
- zapis `tender` / `tender_round` / `tender_win_loss` / `charge`
- auto-award / Alpega live / Freight Bench HTTP / like-for-like SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `tender` / `tender_round` / `party`
