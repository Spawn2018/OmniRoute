# Pobranie COD

Na `/cod` zapisujesz **znacznik** pobrania na zleceniu. To nie kwota i nie rozliczenie Fali F.

1. Na `/shipments` zapisz zlecenie.
2. Wejdź na Pobranie COD. Podaj `instruction_code` (snake 2–32) i status (`noted` / `advised` / `collected` / `refused`).
3. `collected` oznacza, że operator odnotował odbiór gotówki u odbiorcy — **nie** zapis pieniędzy. Marża zostaje na `/charges`.
4. „Zapisz instrukcję pobrania” z `source_ref` (`fixture://cod-instruction/…` albo `tenant:manual`).

Czego tu nie ma: Decimal, FV, `bank_payment`, skan POD, kamera, WMS. Proof of delivery to leftover D4b (`shipment_document`), nie ten ekran. `POD` w słowniku to port wyładunku.

Nazwy w kodzie: `cod_instruction` · `instruction_code` · `collection_status` · `source_ref`.
