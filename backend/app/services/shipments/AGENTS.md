# BC shipment (M-35)

Zlecenie per tenant, FK do `quotation` z `party_id`. 210.0 opcjonalny rodzic.
628.0 opcjonalne daty kotwic T7. Nie tracking, nie marża, nie fx×FV.

## Dozwolone zależności
- `app.models.shipment`
- `app.repositories.shipments`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, nbp_rates, organization_calendars,
  operator_decisions)
- zapis `quotation` / `rate_line` / `charge`
- kwoty / marża / float / mnożenie NBP
- HTTP / Temporal
