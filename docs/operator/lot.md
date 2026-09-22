# Odcinek lotniczy

Na `/air` zostaje lista portów z `airport` w `function_flags`. Osobno zapisujesz odcinek na zleceniu — noga z opcjonalnym numerem HAWB/MAWB albo nadaniem z puli prefiksu. E-rates air zapisujesz w katalogu ofert z kanału.

1. Zapisz zlecenie na `/shipments`. Dla każdego końca zapisz lokalizację `unlocode` na `/locations` wskazującą lotnisko (ta tablica albo `/ports`).
2. Na `/organization-settings` ustaw `hawb_number_prefix` i `mawb_number_prefix` (1–16 znaków A–Z 0–9 . _ -), tak jak prefiks oferty.
3. Wejdź na Lotniczy. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`). HAWB i MAWB są opcjonalne przy zapisie (2–32 litery, cyfry, myślnik).
4. „Zapisz odcinek lotniczy” wiąże te wskazania z `leg_kind=air`. Strefa pocztowa albo port bez flagi `airport` odrzuca. Drugi odcinek `air` na to samo zlecenie też. Numer na odcinku drogowym odrzuca.
5. Na liście odcinków „Nadaj HAWB” / „Nadaj MAWB” bierze prefiks z ustawień i dopisuje cztery cyfry (kolejny numer liczy baza). Drugie kliknięcie nie zmienia numeru. Brak prefiksu odrzuca.
6. E-rates air: wejdź na `/channel-quotes`, wybierz tryb `air`, wklej armatora i dwa porty z flagą `airport`, kwotę Decimal i datę. Tryb `other` zostaje dla oceanu. System nie woła IATA.
7. Odcinki `road`, `rail`, `china_rail` i `ocean_lcl` zostają osobnymi wierszami. System nie woła IATA i nie liczy cyfry kontrolnej.

Czego tu nie ma: cyfra kontrolna IATA, HTTP IATA, mapa, PDF. Marża zostaje na `/charges`. Konosament morski zostaje na `/ocean-bills`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `air` · `hawb_no` · `mawb_no` · `hawb_number_prefix` · `mawb_number_prefix` · `channel_quote` · `transport_mode` · `airport` · `source_ref`.
