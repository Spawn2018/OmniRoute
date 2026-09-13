# Operator: ledger wyniku

Katalog HITL dla faktu (`eta` / `rate` / `route` / `other`).
Zapisujesz kontekst BC, UUID encji, UUID podpowiedzi (jako dana, nie powiązanie)
oraz `actual_value` — liczbę dziesiętną tego, co się naprawdę stało.

`amount`, `margin` i liczby zmiennoprzecinkowe są odrzucane. Zmiana wiersza =
nowy rekord (brak UPDATE). System nie liczy tu CRPS ani MAE — to osobny, późniejszy
krok. Ledger podpowiedzi (`suggestion_ledger`) zostaje osobnym katalogiem.
