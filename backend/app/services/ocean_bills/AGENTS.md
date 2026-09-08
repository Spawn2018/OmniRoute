# BC ocean_bill (D6)

Znacznik HBL/MBL per tenant, FK do `shipment`. Nie PDF, nie booking, nie druga tabela LCL.

## Dozwolone zależności
- `app.models.ocean_bill`
- `app.repositories.ocean_bills`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, geography)
- zapis `shipment` / `charge` / `shipment_leg`
- kwoty / marża / float / Decimal
- HTTP / PDF
