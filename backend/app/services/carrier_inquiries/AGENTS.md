# BC carrier_inquiry (M-30)

Ślad kupna: operator zapisał zapytanie do `network_member`. Nie RFQ sprzedaży. Nie live HTTP.

## Dozwolone zależności
- `app.models.carrier_inquiry`
- `app.repositories.carrier_inquiries`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `rate_line` / `charge` / `network` / `channel_quote`
- kwoty / marża / float
- HTTP / scraping
