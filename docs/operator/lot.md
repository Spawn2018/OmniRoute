# Odcinek lotniczy

Na `/air` zostaje lista portów z `airport` w `function_flags`. Osobno zapisujesz odcinek na zleceniu — to noga, nie list HAWB.

1. Zapisz zlecenie na `/shipments`. Dla każdego końca zapisz lokalizację `unlocode` na `/locations` wskazującą lotnisko (ta tablica albo `/ports`).
2. Wejdź na Lotniczy. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`).
3. „Zapisz odcinek lotniczy” wiąże te wskazania z `leg_kind=air`. Strefa pocztowa albo port bez flagi `airport` odrzuca. Drugi odcinek `air` na to samo zlecenie też.
4. Odcinki `road`, `rail`, `china_rail` i `ocean_lcl` zostają osobnymi wierszami. System nie woła IATA.

Czego tu nie ma: HAWB, MAWB, pule numerów, e-rates, mapa, HTTP. Marża zostaje na `/charges`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `air` · `airport` · `source_ref`.
