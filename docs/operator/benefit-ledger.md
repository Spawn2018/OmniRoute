# Operator: ledger oszczędności

Katalog HITL na zaoszczędzony czas i pieniądze.
Zapisujesz kod wiersza, metodę punktu odniesienia, godziny i kwotę
z walutą — to są dane, które wpisujesz sam.

Bez metody liczba jest nieweryfikowalna. System nie liczy oszczędności
z `charge`, z ledgeru wyniku ani z przebiegu what-if.
`margin` jest odrzucany: marża zostaje tylko na `charge`.
Zmiana wiersza = nowy rekord (brak UPDATE).
Kwoty i godziny wpisujesz jako tekst dziesiętny, nie jako liczbę zmiennoprzecinkową.
