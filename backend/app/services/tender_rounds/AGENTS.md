# BC tender_round (G2.3)

Runda przetargu per tenant. Nie data room. Nie auto-award. Nie kwota.

## Dozwolone zależności
- `app.models.tender_round`
- `app.repositories.tender_rounds`
- `app.domain`

## Zakaz
- import innych BC services (tenders, tender_lots, tender_lanes, quotations, charges)
- zapis `tender` / `tender_lot` / `charge`
- auto-award / kwota / marża / float
- HTTP / TED scrape
