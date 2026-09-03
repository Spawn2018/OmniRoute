# BC shipment (M-35)

Zlecenie per tenant, FK do `quotation` z `party_id`. Nie tracking, nie marża.

## Dozwolone zależności
- `app.models.shipment`
- `app.repositories.shipments`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, operator_decisions)
- zapis `quotation` / `rate_line` / `charge`
- kwoty / marża / float
- HTTP / Temporal
