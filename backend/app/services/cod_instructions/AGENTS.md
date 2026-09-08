# BC cod_instruction (D4)

Znacznik pobrania COD per tenant, FK do `shipment`. Nie kwota, nie rozliczenie F, nie POD portu.

## Dozwolone zależności
- `app.models.cod_instruction`
- `app.repositories.cod_instructions`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, sales_invoices)
- zapis `shipment` / `charge` / `sales_invoice`
- kwoty / marża / float / Decimal
- HTTP
