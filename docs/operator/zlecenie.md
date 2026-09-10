# Zlecenie

Wycena z kontrahentem to jeszcze nie zlecenie. Zlecenie powstaje dopiero gdy je **zapiszesz** na `/shipments`.

1. Przyjmij albo odrzuć ofertę na `/quotations` (szyna decyzji). To nie tworzy zlecenia samo z siebie.
2. Wejdź na zlecenia. Wklej `quotation_id` wyceny, która ma kontrahenta, oraz `source_ref` zapisu (`fixture://shipment/…` albo `tenant:manual`). Opcjonalnie wpisz twardy numer `shipment_ref` (`omni://shipment/…` albo `fixture://shipment-ref/…`). Puste pole = zlecenie bez numeru. Opcjonalnie wskaż zlecenie główne (`parent_shipment_id`) i rodzaj (`drayage` / `oncarriage` / `leg_subcontract` / `other`).
3. „Zapisz zlecenie” wstawia wiersz `shipment`. Jedna wycena — jedno zlecenie. Kwota i marża zostają na wycenie i na `charge`. Rodzic bez rodzaju albo rodzaj bez rodzica jest odrzucany.
4. Wycena bez kontrahenta jest odrzucana. Drugi zapis na tę samą wycenę też. Ten sam `shipment_ref` u tego tenanta też. Rodzic musi być zleceniem tego tenanta.
5. Na tym samym ekranie zapiszesz przejazd. Drugi kierowca (`driver2_id`) jest opcjonalny i musi być innym zasobem rodzaju `driver` niż pierwszy. Puste pole = brak drugiego fotela. Ten sam UUID jest odrzucany. Opcjonalna etykieta trasy (`route_label`) to tekst, nie kilometry.
6. Punkt załadunku może dostać opcjonalny kod grupy (`stop_group_code`). Ten sam kod na kilku punktach tego zlecenia = jedna grupa. Puste pole = punkt bez grupy. Nie osobna tabela. Nie mapa. Opcjonalna notatka dla kierowcy (`notes_for_driver`) to tekst na punkcie. Opcjonalna waga (`weight_kg`) to kilogramy HITL (Decimal), nie VGM i nie liczenie w przeglądarce. Opcjonalna ilość (`quantity`) to liczba całkowita HITL (≥ 0), nie opakowanie i nie plomba. Opcjonalny kod opakowania (`packaging_code`) to tekst HITL (do 32 znaków), nie słownik FK i nie plomba.

Czego tu nie ma: generator `GD/2026`, QR, PDF, ZPL, 409 wyjazdu, auto-booking po Przyjmij, bramka sankcji, suma przychodu z podzleceń, liczenie w przeglądarce.

Nazwy w kodzie: `shipment` · `quotation_id` · `party_id` z wyceny · `shipment_ref` · `parent_shipment_id` · `relation_kind` · `trip` · `driver2_id` · `route_label` · `stop` · `stop_group_code` · `notes_for_driver` · `weight_kg` · `quantity` · `packaging_code`.
