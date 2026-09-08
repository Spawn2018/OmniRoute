# BC tender_lane (G2.2)

Korytarz partii przetargu per tenant. Nie runda. Nie auto-award. Nie kwota.

## Dozwolone zależności
- `app.models.tender_lane`
- `app.repositories.tender_lanes`
- `app.domain`

## Zakaz
- import innych BC services (tender_lots, tenders, geography, quotations, charges)
- zapis `tender_lot` / `tender` / `port` / `charge`
- auto-award / kwota / marża / float
- HTTP / TED scrape
