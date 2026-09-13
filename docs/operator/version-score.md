# Operator: wynik wersji

To jest odczyt, nie zapis.

Widok grupuje pary z wyniku przedziału według wersji modelu z ledgeru
podpowiedzi. Postgres liczy liczbę par oraz średnie MAE i CRPS.

Nie wpisujesz średnich. Nie przełączasz tu modelu na champion.
Mniejsza średnia CRPS oznacza lepsze dopasowanie przedziału do faktu
— decyzja, którą wersję zostawić, jest twoja.

Dryf w czasie nie jest na tym ekranie. Ledger predykcji nie przyjmuje już
wpisanego CRPS — liczone liczby są na wyniku przedziału.
