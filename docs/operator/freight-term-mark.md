# Operator: warunek frachtu

Katalog HITL dla warunku frachtu (`prepaid` / `collect` / `third_party` / `other`).
Zapisujesz kod, `term_kind` i `source_ref`. To nie jest kolumna na zleceniu
ani auto z Incoterms.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
