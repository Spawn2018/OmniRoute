# Przesyłka

Na `/consignments` zapisujesz **przesyłkę** (`consignment`) na zleceniu. To nie paczka QR i nie podzlecenie.

1. Na `/shipments` zapisz zlecenie.
2. Wejdź na Przesyłki. Wklej `shipment_id` oraz `consignment_ref` (2–64 litery, cyfry, `.` `_` `:` `-`) i `source_ref` (`fixture://consignment/…` albo `tenant:manual`).
3. „Zapisz przesyłkę” wstawia wiersz. Na jednym zleceniu możesz mieć wiele przesyłek (LTL/LCL). Unique FTL=1 zostaje leftover.

Czego tu nie ma: paczka `/shipment-packages`, mapa, unique jednego wiersza na FTL, SQL marży, live HTTP.

Nazwy w kodzie: `consignment` · `consignment_ref` · `shipment_id` · `source_ref` · `/consignments`.
