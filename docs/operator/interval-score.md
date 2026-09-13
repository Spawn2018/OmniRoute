# Operator: wynik przedziału

To jest odczyt, nie zapis.

Widok łączy ledger podpowiedzi z ledgerem faktu po tym samym tenantcie
i UUID podpowiedzi. Postgres liczy dwie liczby: MAE od środka przedziału
oraz CRPS dla rozkładu jednostajnego na tym przedziale.

Nie wpisujesz CRPS ani MAE. Formularza nie ma. Jeśli pary nie widać,
najpierw zapisz podpowiedź, potem fakt z tym samym UUID.

Wpisane CRPS na ledgerze predykcji jest historią — nowy wiersz go nie przyjmuje. Ten widok
go nie zastępuje i nic tam nie zapisuje.

`amount`, marża i liczby zmiennoprzecinkowe nie wchodzą w ten odczyt.
