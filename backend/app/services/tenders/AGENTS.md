# BC tender (G2.0)

Nagłówek przetargu per tenant. Nie loty. Nie auto-award. Nie kwota.

## Dozwolone zależności
- `app.models.tender`
- `app.repositories.tenders`
- `app.domain`

## Zakaz
- import innych BC services (parties, quotations, charges, tender_quotes)
- zapis `party` / `quotation` / `charge` / `tender_quote`
- auto-award / kwota / marża / float
- HTTP / TED scrape
