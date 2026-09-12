# BC pallet_pool_mark (EXP2.17)

HITL katalog znacznika puli palet per tenant. mark_code + pool_kind
chep|lpr|epal|other + source_ref. Nie giełda. Nie depozyt.
Obok `pallet_balance` (D7) — tu rodzaj puli, nie integer sztuk.

## Dozwolone zależności
- `app.models.pallet_pool_mark`
- `app.repositories.pallet_pool_marks`
- `app.domain`

## Zakaz
- import innych BC services (pallet_balances, parties, charges, extraction)
- zapis `pallet_balance` / `party` / `charge` / `extraction_draft`
- giełda Chep/LPR · HTTP pool · depozyt · euro ledger
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
