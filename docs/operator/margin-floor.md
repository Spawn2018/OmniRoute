# Operator: podłoga marży

Katalog HITL na minimalną marżę na korytarzu (para UN/LOCODE).
Zapisujesz kod, origin, destination, kwotę z walutą i wskazanie źródła —
to są dane, które wpisujesz sam.

Przy zapisie opłaty (`POST /charges`) możesz podać tę samą parę UN/LOCODE.
Gdy w katalogu jest podłoga w tej walucie i marża (sprzedaż − kupno) jest
niższa — system odmawia zapisem **409**. Bez pary w body — bez sprawdzenia.
Marża nadal liczy się tylko na `charge`. Zmiana wiersza podłogi = nowy rekord
(brak UPDATE). Kwoty wpisujesz jako tekst dziesiętny, nie float.
S11 (mail zamiast 409) = leftover.
