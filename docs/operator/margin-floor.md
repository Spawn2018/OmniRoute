# Operator: podłoga marży

Katalog HITL na minimalną marżę na korytarzu (para UN/LOCODE).
Zapisujesz kod, origin, destination, kwotę z walutą i wskazanie źródła —
to są dane, które wpisujesz sam.

System nie egzekwuje 409 przy zapisie `charge` w tym plasterze.
Marża zostaje tylko na `charge`. Zmiana wiersza = nowy rekord (brak UPDATE).
Kwoty wpisujesz jako tekst dziesiętny, nie jako liczbę zmiennoprzecinkową.
