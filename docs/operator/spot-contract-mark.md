# Operator: spot / contract

Katalog HITL dla trybu transakcji na wycenie (`spot` / `contract` / `other`).
Zapisujesz kod, `deal_kind` i `source_ref`. To nie jest FK quotation ani cargo_value.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz spot_or_contract bezposrednio na wycenie.
