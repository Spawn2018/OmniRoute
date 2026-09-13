# Zdarzenie pozycji (BR2.0)

Operator zapisuje katalogowe zdarzenie: kod, `source_kind`
(`gps` / `manual` / `other`) i `source_ref`. To dane HITL,
nie live GPS i nie `tracking_event` na zleceniu.

Nie liczy kwot. Marża nadal tylko na `charge`.
Współrzędne i poll zostają leftover.

Ścieżka UI: `/position-events`.
