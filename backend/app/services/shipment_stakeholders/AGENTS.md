# BC shipment_stakeholder (I2)

Strona zlecenia per tenant: rola + party_id. Nie dispatch, nie EXP1.

## Dozwolone zależności
- `app.models.shipment_stakeholder`
- `app.repositories.shipment_stakeholders`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges)
- zapis `shipment` / `party` / `charge`
- kwoty / marża / float
- HTTP / 409 dispatch / sold_to
