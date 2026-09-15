# Poziom alokacji (AI7.0)

Operator zapisuje otwarty słownik poziomów podziału kosztów: `level_code`
(snake 2–32) i `source_ref` (`tenant:manual` albo `fixture://allocation-level/…`).
Nowy poziom = nowy wiersz. To dane HITL, nie silnik SQL i nie druga marża.

Marża nadal tylko na `charge`. `allocation_key` i `cost_category_mark` zostają osobno.

Ścieżka UI: `/allocation-levels`.
