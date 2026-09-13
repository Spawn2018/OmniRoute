# Operator: bid decision

Katalog HITL dla decyzji oferty (`go` / `no_go` / `hold` / `other`).
Zapisujesz kod, `decision_kind` i `source_ref`. To nie jest kolumna na quotation ani auto-award.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz bid_decision bezposrednio na wycenie.
