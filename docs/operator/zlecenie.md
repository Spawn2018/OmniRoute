# Zlecenie

Wycena z kontrahentem to jeszcze nie zlecenie. Zlecenie powstaje dopiero gdy je **zapiszesz** na `/shipments`.

1. Przyjmij albo odrzuć ofertę na `/quotations` (szyna decyzji). To nie tworzy zlecenia samo z siebie.
2. Wejdź na zlecenia. Wklej `quotation_id` wyceny, która ma kontrahenta, oraz `source_ref` zapisu (`fixture://shipment/…` albo `tenant:manual`).
3. „Zapisz zlecenie” wstawia wiersz `shipment`. Jedna wycena — jedno zlecenie. Kwota i marża zostają na wycenie i na `charge`.
4. Wycena bez kontrahenta jest odrzucana. Drugi zapis na tę samą wycenę też.

Czego tu nie ma: numer `GD/2026`, odcinki, tracking, HBL, auto-booking po Przyjmij, bramka sankcji, liczenie w przeglądarce.

Nazwy w kodzie: `shipment` · `quotation_id` · `party_id` z wyceny.
