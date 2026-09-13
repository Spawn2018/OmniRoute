# Operator: wynik okna wersji

To jest odczyt, nie zapis.

Widok grupuje pary z wyniku przedziału według wersji modelu i dnia UTC
z ledgeru podpowiedzi. Postgres liczy liczbę par oraz średnie MAE i CRPS
dla każdego dnia.

Nie wpisujesz średnich. Nie ustawiasz tu progu ani flagi dryfu.
Nie przełączasz modelu na champion. Szereg pokazuje, jak wersja zachowuje
się z dnia na dzień — decyzja, co z tym zrobić, jest twoja.

Ranking wszystkich par bez dnia zostaje na wyniku wersji. Wpisane CRPS
na ledgerze predykcji zostaje osobnym katalogiem.
