# Przesyłka

Na `/consignments` zapisujesz **przesyłkę** (`consignment`) na zleceniu. To nie paczka QR i nie podzlecenie.

1. Na `/shipments` zapisz zlecenie.
2. Wejdź na Przesyłki. Wklej `shipment_id` oraz `consignment_ref` (2–64 litery, cyfry, `.` `_` `:` `-`) i `source_ref` (`fixture://consignment/…` albo `tenant:manual`).
3. Opcjonalnie `load_kind`: `ftl` albo `ltl`. Przy `ftl`, gdy zlecenie ma już przesyłkę — system odmawia **409**. Bez pola albo `ltl` — wiele przesyłek na zleceniu wolno (LTL/LCL).
4. „Zapisz przesyłkę” wstawia wiersz.

Czego tu nie ma: paczka `/shipment-packages`, mapa, unique w bazie na FTL, kolumna trybu na zleceniu, SQL marży, live HTTP.

Nazwy w kodzie: `consignment` · `consignment_ref` · `shipment_id` · `source_ref` · `load_kind` · `/consignments`.
