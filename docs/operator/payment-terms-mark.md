# Operator: warunki płatności

Katalog HITL dla warunków płatności na zleceniu (`net` / `prepaid` / `other`).
Zapisujesz kod, `terms_kind` i `source_ref`. To nie jest liczba dni ani skonto.

`amount`, `margin`, `score` i `days` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz `party.payment_terms_days` ani kolumny na shipment.
