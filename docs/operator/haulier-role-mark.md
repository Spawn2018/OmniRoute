# Operator: rola przewoznika

Katalog HITL dla roli przewoznika na zleceniu (`booked` / `actual` / `other`).
Zapisujesz kod, `role_kind` i `source_ref`. To nie jest FK party na shipment ani cargo_value.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz booked_carrier vs actual_haulier bezposrednio na zleceniu.
