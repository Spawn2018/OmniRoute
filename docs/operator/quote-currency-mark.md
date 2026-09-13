# Operator: quote currency

Katalog HITL dla waluty oferty (`go` / `no_go` / `hold` / `other`).
Zapisujesz kod, `currency_kind` i `source_ref`. To nie jest kolumna na quotation ani NBP.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz bid_decision bezposrednio na wycenie.
