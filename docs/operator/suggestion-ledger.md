# Operator: ledger podpowiedzi

Katalog HITL dla podpowiedzi systemu.
Rodzaj (`suggestion_kind`) musi już istnieć w słowniku rodzajów podpowiedzi.
Nowy rodzaj zapisujesz najpierw tam, potem tu.

Zapisujesz kontekst BC, UUID encji (jako dana, nie powiązanie), przedział
dziesiętny, wersję modelu i promptu, reakcję (`accept` / `modify` / `reject`)
oraz `changed_to`. Przy accept i reject wpisz `none`. Przy modify — na co
zmieniłeś, nie `none`.

`amount`, `margin` i liczby zmiennoprzecinkowe są odrzucane. Zmiana wiersza =
nowy rekord (brak UPDATE). Model językowy tu nic nie zapisuje i nic nie liczy.
Ledger predykcji (`prediction_ledger`) zostaje osobnym katalogiem przedziału; CRPS/MAE liczy wynik przedziału.
