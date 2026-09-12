# Operator: centrum zysku/kosztu/projektu

Katalog HITL dla centrum zysku, kosztu i projektu (`profit` / `cost` / `project` / `other`).
Zapisujesz kod, `center_kind` i `source_ref`. To nie jest kolumna na zleceniu
ani allocation SQL z cost_allocation_mark.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
