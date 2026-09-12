# Operator: referencja PO klienta

Katalog HITL dla referencji PO klienta (`customer_po` / `release` / `call_off` / `other`).
Zapisujesz kod, `ref_kind` i `source_ref`. To nie jest purchase_order CT1
ani kolumna na zleceniu.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
