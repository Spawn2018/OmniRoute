# Zlecenie

Wycena z kontrahentem to jeszcze nie zlecenie. Zlecenie powstaje dopiero gdy je **zapiszesz** na `/shipments`.

1. Przyjmij albo odrzuć ofertę na `/quotations` (szyna decyzji). To nie tworzy zlecenia samo z siebie.
2. Wejdź na zlecenia. Wklej `quotation_id` wyceny, która ma kontrahenta, oraz `source_ref` zapisu (`fixture://shipment/…` albo `tenant:manual`). Opcjonalnie wpisz twardy numer `shipment_ref` (`omni://shipment/…` albo `fixture://shipment-ref/…`). Puste pole = zlecenie bez numeru. Opcjonalnie wskaż zlecenie główne (`parent_shipment_id`) i rodzaj (`drayage` / `oncarriage` / `leg_subcontract` / `other`).
3. „Zapisz zlecenie” wstawia wiersz `shipment`. Jedna wycena — jedno zlecenie. Kwota i marża zostają na wycenie i na `charge`. Rodzic bez rodzaju albo rodzaj bez rodzica jest odrzucany.
4. Wycena bez kontrahenta jest odrzucana. Drugi zapis na tę samą wycenę też. Ten sam `shipment_ref` u tego tenanta też. Rodzic musi być zleceniem tego tenanta.
5. Na tym samym ekranie zapiszesz przejazd. Drugi kierowca (`driver2_id`) jest opcjonalny i musi być innym zasobem rodzaju `driver` niż pierwszy. Puste pole = brak drugiego fotela. Ten sam UUID jest odrzucany. Nie km.
6. Punkt załadunku może dostać opcjonalny kod grupy (`stop_group_code`). Ten sam kod na kilku punktach tego zlecenia = jedna grupa. Puste pole = punkt bez grupy. Nie osobna tabela. Nie mapa.

Czego tu nie ma: generator `GD/2026`, QR, PDF, ZPL, 409 wyjazdu, auto-booking po Przyjmij, bramka sankcji, suma przychodu z podzleceń, liczenie w przeglądarce.

Nazwy w kodzie: `shipment` · `quotation_id` · `party_id` z wyceny · `shipment_ref` · `parent_shipment_id` · `relation_kind` · `trip` · `driver2_id` · `stop` · `stop_group_code`.
