# Operator: ledger wyniku

Katalog HITL dla faktu.
Rodzaj (`outcome_kind`) musi już istnieć w słowniku rodzajów wyniku.
Nowy rodzaj zapisujesz najpierw tam, potem tu.

Zapisujesz kontekst BC, UUID encji, UUID podpowiedzi (jako dana, nie powiązanie)
oraz `actual_value` — liczbę dziesiętną tego, co się naprawdę stało.

`amount`, `margin` i liczby zmiennoprzecinkowe są odrzucane. Zmiana wiersza =
nowy rekord (brak UPDATE). System nie liczy tu CRPS ani MAE — to osobny, późniejszy
krok. Ledger podpowiedzi (`suggestion_ledger`) zostaje osobnym katalogiem.
