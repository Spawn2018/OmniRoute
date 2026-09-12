# Operator: dual ledger

Katalog HITL dla dwóch ledgerów operacyjnego i finansowego
(`ops` / `finance` / `tax` / `other`).
Zapisujesz kod, `ledger_kind` i `source_ref`. To nie jest druga marża
ani SQL na charge.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
