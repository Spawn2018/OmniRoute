# Operator: podłoga marży

Katalog HITL na minimalną marżę na korytarzu (para UN/LOCODE).
Zapisujesz kod, origin, destination, kwotę z walutą i wskazanie źródła —
to są dane, które wpisujesz sam.

Przy zapisie opłaty (`POST /charges`) możesz podać tę samą parę UN/LOCODE.
Gdy w katalogu jest podłoga w tej walucie i marża (sprzedaż − kupno) jest
niższa — system odmawia zapisem **409** i jednocześnie zakłada (albo wznawia)
oczekującą decyzję na szynie S11 (`/decisions`) dla tej podłogi. W odpowiedzi
409 dostajesz `decision_id`.

Po **Akceptuj** na `/decisions` możesz ponowić `POST /charges` z tym samym
ładunkiem oraz polem `floor_decision_id` = id zaakceptowanej decyzji —
wtedy zapis poniżej podłogi przechodzi. Odrzucona albo wciąż pending decyzja
nie odblokowuje zapisu.

Bez pary w body — bez sprawdzenia. Marża nadal liczy się tylko na `charge`.
Zmiana wiersza podłogi = nowy rekord (brak UPDATE). Kwoty wpisujesz jako tekst
dziesiętny, nie float.
