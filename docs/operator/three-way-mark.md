# Operator: znacznik 3-way

Katalog HITL dla znacznika postawy 3-way (nabywca / sprzedawca / przewoźnik / inne).
Zapisujesz kod, `way_kind` i `source_ref`. To nie jest tuple OpenFGA per strona
ani wspólny SELECT cross-shipper (leftover CT11 / `collaboration_mark`).

`amount`, `tuple` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
