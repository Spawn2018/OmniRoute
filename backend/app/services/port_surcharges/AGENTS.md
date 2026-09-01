# BC port_surcharge (M-18)

Katalog extra portowego per tenant: warunek to dane, kwota Decimal, nie marża.

## Dozwolone zależności
- `app.models.port_surcharge`
- `app.models.port`
- `app.repositories.port_surcharges`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `rate_line` / `charge`
- ewaluacja `applies_when`
- liczenie marży / float na kwocie
