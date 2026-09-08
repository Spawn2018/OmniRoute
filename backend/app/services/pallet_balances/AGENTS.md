# BC pallet_balance (D7)

Saldo Chep/LPR per tenant, FK do `party`. Nie giełda, nie depozyt, nie kwota.

## Dozwolone zależności
- `app.models.pallet_balance`
- `app.repositories.pallet_balances`
- `app.domain`

## Zakaz
- import innych BC services (parties, charges, shipments)
- zapis `party` / `charge` / `shipment`
- kwoty / marża / float / Decimal
- HTTP / giełda
