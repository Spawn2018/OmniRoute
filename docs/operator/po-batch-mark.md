# Operator: znacznik PO batch

Katalog HITL dla znacznika batch/lot na linii zamówienia zakupu
(`batch` / `lot` / `serial` / `other`).
Zapisujesz kod, `batch_kind` i `source_ref`. To nie jest live EDI ani
auto shipment, ani zapis do `purchase_order` / `po_line`.

`amount`, `qty` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
