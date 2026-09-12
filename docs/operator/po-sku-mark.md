# Operator: znacznik PO SKU

Katalog HITL dla znacznika SKU na linii zamówienia zakupu
(`sku` / `gtin` / `customer_sku` / `other`).
Zapisujesz kod, `sku_kind` i `source_ref`. To nie jest live EDI ani
auto shipment, ani zapis do `purchase_order` / `po_line`.

`amount`, `qty` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
