# Operator: diversion

Katalog HITL dla postawy diversion na zleceniu (`diversion` / `reroute` / `other`).
Zapisujesz kod, `stance_kind` i `source_ref`. To nie jest FK shipment ani cargo_value.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz diversion_of_shipment_id bezposrednio na zleceniu.
