# BC tender_quote (P6)

Ważność + limit orderów z oferty per tenant. Nie auto-award. Nie obiekt tender G2.

## Dozwolone zależności
- `app.models.tender_quote`
- `app.repositories.tender_quotes`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, channel_quotes, trips)
- zapis `quotation` / `charge` / `channel_quote`
- auto-award / kwota / marża / float
- HTTP / TED scrape
