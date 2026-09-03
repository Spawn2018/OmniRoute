# Odcinek kolej z Chin

Na `/china-rail` zostaje lista portów `CN` z flagą `rail`. Osobno zapisujesz odcinek na zleceniu — to noga, nie korytarz.

1. Zapisz zlecenie na `/shipments`. Dla każdego końca zapisz lokalizację `unlocode` na `/locations` wskazującą port chiński z flagą `rail` (ta tablica albo `/ports`).
2. Wejdź na Kolej z Chin. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`).
3. „Zapisz odcinek kolej z Chin” wiąże te wskazania z `leg_kind=china_rail`. Strefa pocztowa, port bez `rail` albo kraj inny niż CN odrzuca. Drugi odcinek `china_rail` na to samo zlecenie też.
4. Odcinek `rail` na `/rail` i `road` na `/road` zostają osobnymi wierszami. System nie liczy trasy.

Czego tu nie ma: korytarz, rozkład CR, HTTP, mapa, GPS, drobnica. Marża zostaje na `/charges`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `china_rail` · `country_code` · `source_ref`.
