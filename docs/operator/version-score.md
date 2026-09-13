# Operator: wynik wersji

To jest odczyt, nie zapis.

Widok grupuje pary z wyniku przedziału według wersji modelu z ledgeru
podpowiedzi. Postgres liczy liczbę par oraz średnie MAE i CRPS.

Nie wpisujesz średnich. Nie przełączasz tu modelu na champion.
Mniejsza średnia CRPS oznacza lepsze dopasowanie przedziału do faktu
— decyzja, którą wersję zostawić, jest twoja.

Dryf w czasie nie jest na tym ekranie. Wpisane CRPS na ledgerze predykcji
zostaje osobnym katalogiem.
