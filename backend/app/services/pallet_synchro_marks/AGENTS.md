# BC pallet_synchro_mark (D7c leftover)

HITL katalog stance synchro salda↔ledger per tenant. mark_code +
synchro_kind aligned|drift|held|other + source_ref. Nie auto-UPDATE.
Nie giełda. Nie suma ledgeru.

## Dozwolone zależności
- `app.models.pallet_synchro_mark`
- `app.repositories.pallet_synchro_marks`
- `app.domain`

## Zakaz
- import innych BC services (pallet_balances, pallet_ledgers, parties, charges, extraction)
- zapis `pallet_balance` / `pallet_ledger` / `party` / `charge` / `extraction_draft`
- auto-UPDATE salda / SQL sumy ledgeru / giełda live
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `pallet_balance` / `pallet_ledger` / `party`
