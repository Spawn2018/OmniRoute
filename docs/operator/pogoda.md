# Pogoda

Na `/weather-observations` zapisujesz **obserwację pogody** tenanta (warunek, stacja UN/LOCODE, czas ze strefą). To nie feed Open-Meteo i nie silnik ETA.

1. Wejdź na Pogoda. Wybierz warunek z listy (`clear` / `rain` / `snow` / `wind` / `fog` / `ice` / `other`) i wpisz stację (5 znaków, np. `PLGDY`).
2. Podaj czas ISO-8601 ze strefą oraz `source_ref` (`fixture://weather-observation/…` albo `tenant:manual`). Dostawca to tylko `hitl`.
3. „Zapisz pogodę”.

Czego tu nie ma: Open-Meteo, IMGW, DWD, lat/lng, geometria przejazdu, GPS, myto, suma w przeglądarce. Dwa ETA zostają na `/shipments`. Marża zostaje na `/charges`.

Nazwy w kodzie: `weather_observation` · `condition_code` · `station_unlocode` · `observed_at` · `provider_code` · `source_ref`.
