# BC operational_exception (M-37)

Wyjatek operacyjny per tenant, FK do `shipment`. Nie mapa, nie czas przybycia, nie AIS.

## Dozwolone zależności
- `app.models.operational_exception`
- `app.repositories.operational_exceptions`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, geography)
- zapis `shipment` / `quotation` / `charge`
- kwoty / marża / float / czas przybycia liczony
- HTTP / mapa
