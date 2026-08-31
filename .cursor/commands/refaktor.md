---
description: Slot refaktoryzacyjny z wejściem z metryk
---

Uruchom i zbierz wyniki:
  just complexity   → funkcje powyżej progu 10
  just dup          → duplikacja powyżej 3%
  just dead         → martwy kod
  python scripts/quality/refactor_ratio.py --weeks 4

Zbuduj listę zadań posortowaną po: (liczba wywołań × złożoność).

Dla każdej pozycji zaproponuj konkretną zmianę.
NIE ZMIENIAJ ZACHOWANIA. Testy muszą przejść bez modyfikacji.
Po każdej zmianie uruchom `just test`.

Zatrzymaj się po trzech pozycjach i pokaż wynik.
