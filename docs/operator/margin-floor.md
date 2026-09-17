# Operator: podłoga marży

Katalog HITL na minimalną marżę na korytarzu (para UN/LOCODE).
Zapisujesz kod, origin, destination, kwotę z walutą i wskazanie źródła —
to są dane, które wpisujesz sam.

Na ekranie **Opłaty** (`/charges`) możesz podać opcjonalnie UN origin i
destination oraz — po akceptacji S11 — `floor_decision_id`.

Przy zapisie opłaty (`POST /charges`) z parą UN/LOCODE: gdy w katalogu jest
podłoga w tej walucie i marża (sprzedaż − kupno) jest niższa — system odmawia
zapisem **409** i jednocześnie zakłada (albo wznawia) oczekującą decyzję na
szynie S11 (`/decisions`) dla tej podłogi. W odpowiedzi 409 dostajesz
`decision_id` (UI pokazuje go w komunikacie błędu).

Po **Akceptuj** na `/decisions` możesz ponowić zapis z tym samym ładunkiem oraz
polem `floor_decision_id` = id zaakceptowanej decyzji — wtedy zapis poniżej
podłogi przechodzi. Odrzucona albo wciąż pending decyzja nie odblokowuje zapisu.

Bez pary w body — bez sprawdzenia. Marża nadal liczy się tylko na `charge`.
Zmiana wiersza podłogi = nowy rekord (brak UPDATE). Kwoty wpisujesz jako tekst
dziesiętny, nie float.
