# BC channel_quote (M-19)

Katalog oferty z kanału per tenant: kwota Decimal, nie marża, nie live HTTP.

## Dozwolone zależności
- `app.models.channel_quote`
- `app.models.carrier_profile`
- `app.models.port`
- `app.repositories.channel_quotes`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `rate_line` / `charge`
- HTTP do armatorów
- liczenie marży / float na kwocie
