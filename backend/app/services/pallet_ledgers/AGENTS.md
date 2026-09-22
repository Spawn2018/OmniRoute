# BC pallet_ledger (D7c)

HITL ledger ruchu palet per tenant. movement_code + pallet_kind
chep|lpr|epal + delta_count (integer ze znakiem) + source_ref.
Nie mutuje pallet_balance. Nie giełda. Nie kwota.

## Dozwolone zależności
- `app.models.pallet_ledger`
- `app.repositories.pallet_ledgers`
- `app.domain`

## Zakaz
- import innych BC services (pallet_balances, parties, charges, shipments)
- zapis `pallet_balance` / `party` / `charge` / `shipment`
- auto-przeliczenie salda / giełda HTTP
- kwota / marża / float / Decimal
- HTTP
- UPDATE / DELETE wiersza
