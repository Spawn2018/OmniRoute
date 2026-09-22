# Saldo palet

Na `/pallet-balances` zapisujesz **liczbę sztuk** palet Chep, LPR albo EPAL na kontrahencie. To nie giełda i nie depozyt.

1. Na `/parties` zapisz kontrahenta.
2. Wejdź na Saldo palet. Wybierz `pallet_kind` (`chep` / `lpr` / `epal`) i podaj nieujemną liczbę całkowitą sztuk.
3. „Zapisz saldo palet” z `source_ref` (`fixture://pallet-balance/…` albo `tenant:manual`).

Na `/pallet-ledgers` zapisujesz **ruch** sztuk ze znakiem (wydanie ujemne, zwrot dodatni). Ten wpis **nie** zmienia salda na `/pallet-balances`.

1. Podaj kod ruchu (`movement_code`), rodzaj i deltę całkowitą.
2. „Zapisz ruch palet” z `source_ref` (`fixture://pallet-ledger/…` albo `tenant:manual`).

Czego tu nie ma: giełda palet, live HTTP Chep/LPR, auto-przeliczenie salda z ledgeru, kwota na `charge`.

Nazwy w kodzie: `pallet_balance` · `pallet_ledger` · `pallet_kind` · `unit_count` · `delta_count` · `source_ref`.
