---
description: Slot refaktoryzacyjny z wejściem z metryk
---

Kanon: `docs/PLAN-REALIZACJA.md` § Cel jakości (4,4–5). Ten slot spłaca **stare 3,x** na Grupie A. Nie nowy M-xx. Nie 5,0 na tablicy-odczycie. Nie F9.1.

**Pierwsza komenda (obowiązkowa):** `python scripts/quality/factory_cycle.py --start refactor`

Uruchom i zbierz wyniki:
  just complexity   → funkcje powyżej progu 10
  just dup          → duplikacja powyżej 3%
  just dead         → martwy kod (echo — nie DoD)
  python scripts/quality/refactor_ratio.py --weeks 4

Zbuduj listę zadań posortowaną po: (liczba wywołań × złożoność).
Priorytet Q-E1: katalogi na `catalog-parts` (trzecie powtórzenie). Nie mixin wszystkich modeli.

Dla każdej pozycji zaproponuj konkretną zmianę.
NIE ZMIENIAJ ZACHOWANIA. Testy muszą przejść bez modyfikacji.
Po każdej zmianie uruchom `just test`.

Zatrzymaj się po trzech pozycjach, wypełnij kartę `docs/ops/post-plaster.md`, potem
`python scripts/quality/factory_cycle.py --close` i skill `zamknij-plaster`.
Komentarz tylko *dlaczego*. Autorecenzja „jak senior” nie liczy się do 4,4.
