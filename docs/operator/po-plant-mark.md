# Operator: znacznik PO plant

Katalog HITL dla znacznika plant/batch/SKU na zamówieniu zakupu
(`plant` / `batch` / `sku` / `other`).
Zapisujesz kod, `plant_kind` i `source_ref`. To nie jest live EDI ani
auto shipment, ani zapis do `purchase_order`.

`amount`, `qty` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
