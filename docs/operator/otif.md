# Znacznik OTIF (CT3)

Ekran `/otif-marks` zapisuje zakres OTIF jako dane: kod snake, zakres `pickup` / `delivery` / `sku`, oraz `source_ref`.

To katalog HITL. Nie liczy OTIF%. Nie scoring SQL na stopach ani liniach SKU. Nie kwota i nie marża.

Źródło zapisu: `tenant:manual` albo `fixture://otif-mark/…`. Zły kod albo zakres → błąd walidacji po polsku.

Czego tu nie ma: procent OTIF, 409 na zlecenie, auto shipment, live EDI, mapa. Marża zostaje na `/charges`.
