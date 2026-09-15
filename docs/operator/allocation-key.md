# Klucz alokacji (AI7.0)

Operator zapisuje otwarty słownik kluczy podziału kosztów: `key_code`
(snake 2–32) i `source_ref` (`tenant:manual` albo `fixture://allocation-key/…`).
Nowy klucz = nowy wiersz. To dane HITL, nie silnik SQL i nie druga marża.

Marża nadal tylko na `charge`. `cost_allocation_mark` (tryb) zostaje osobno.

Ścieżka UI: `/allocation-keys`.
