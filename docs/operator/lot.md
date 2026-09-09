# Odcinek lotniczy

Na `/air` zostaje lista portów z `airport` w `function_flags`. Osobno zapisujesz odcinek na zleceniu — noga z opcjonalnym numerem HAWB/MAWB, nie pula IATA.

1. Zapisz zlecenie na `/shipments`. Dla każdego końca zapisz lokalizację `unlocode` na `/locations` wskazującą lotnisko (ta tablica albo `/ports`).
2. Wejdź na Lotniczy. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`). HAWB i MAWB są opcjonalne (2–32 litery, cyfry, myślnik).
3. „Zapisz odcinek lotniczy” wiąże te wskazania z `leg_kind=air`. Strefa pocztowa albo port bez flagi `airport` odrzuca. Drugi odcinek `air` na to samo zlecenie też. Numer na odcinku drogowym odrzuca.
4. Odcinki `road`, `rail`, `china_rail` i `ocean_lcl` zostają osobnymi wierszami. System nie woła IATA i nie nadaje numeru z puli.

Czego tu nie ma: pula M-03, cyfra kontrolna IATA, HTTP, mapa, PDF. Marża zostaje na `/charges`. Konosament morski zostaje na `/ocean-bills`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `air` · `hawb_no` · `mawb_no` · `airport` · `source_ref`.
