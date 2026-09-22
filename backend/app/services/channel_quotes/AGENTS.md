# BC channel_quote (M-19)

Katalog oferty z kanału per tenant: kwota Decimal, `transport_mode`
air|other, nie marża, nie live HTTP / IATA.

## Dozwolone zależności
- `app.models.channel_quote`
- `app.models.carrier_profile`
- `app.models.port`
- `app.repositories.channel_quotes`
- `app.domain`

## Zakaz
- import innych BC services (w tym `shipment_legs`)
- zapis `quotation` / `rate_line` / `charge`
- HTTP do armatorów / IATA
- liczenie marży / float na kwocie
- UPDATE / DELETE wiersza
