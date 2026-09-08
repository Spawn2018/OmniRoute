# BC tender_lot (G2.1)

Partia przetargu per tenant. Nie korytarz. Nie auto-award. Nie kwota.

## Dozwolone zależności
- `app.models.tender_lot`
- `app.repositories.tender_lots`
- `app.domain`

## Zakaz
- import innych BC services (tenders, quotations, charges, tender_quotes)
- zapis `tender` / `quotation` / `charge`
- auto-award / kwota / marża / float
- HTTP / TED scrape
