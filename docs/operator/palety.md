# Saldo palet

Na `/pallet-balances` zapisujesz **liczbę sztuk** palet Chep, LPR albo EPAL na kontrahencie. To nie giełda i nie depozyt.

1. Na `/parties` zapisz kontrahenta.
2. Wejdź na Saldo palet. Wybierz `pallet_kind` (`chep` / `lpr` / `epal`) i podaj nieujemną liczbę całkowitą sztuk.
3. „Zapisz saldo palet” z `source_ref` (`fixture://pallet-balance/…` albo `tenant:manual`).

Czego tu nie ma: giełda palet, live HTTP Chep/LPR, ujemny ledger, kwota na `charge`.

Nazwy w kodzie: `pallet_balance` · `pallet_kind` · `unit_count` · `source_ref`.
