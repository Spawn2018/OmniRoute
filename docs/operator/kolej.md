# Odcinek kolejowy

Na `/rail` zostaje lista portów z flagą `rail`. Osobno zapisujesz odcinek na zleceniu — to noga, nie rozkład.

1. Zapisz zlecenie na `/shipments`. Dla każdego końca zapisz lokalizację `unlocode` na `/locations` wskazującą port z flagą `rail` (katalog portów: `/ports` albo ta tablica).
2. Wejdź na Kolej intermodalna. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`).
3. „Zapisz odcinek kolejowy” wiąże te wskazania z `leg_kind=rail`. Strefa pocztowa albo port bez `rail` odrzuca. Drugi odcinek `rail` na to samo zlecenie też.
4. Odcinek drogowy na `/road` zostaje osobnym wierszem. System nie liczy kilometrów.

Czego tu nie ma: wagon, CIM, mapa, GPS, kolej z Chin, drobnica. Marża zostaje na `/charges`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `unlocode` · `function_flags` · `source_ref`.
