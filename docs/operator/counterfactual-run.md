# Operator: przebieg what-if

Katalog HITL dla nazwanego przebiegu „co by było gdyby”.
Zapisujesz kod scenariusza, punkt odniesienia, listę dźwigni i wynik
jako tekst — to są dane, nie wyliczenie.

`amount` i `margin` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
System nie uruchamia tu silnika what-if i nie liczy oszczędności w pieniądzu.
Przebieg musi wskazywać istniejącą migawkę planu tego tenanta.
Powtórka (`/what-if-replays`) tylko odtwarza kody i UUID — nic nie liczy.

Znacznik rodzaju (`what_if_mark`) zostaje osobnym katalogiem.
