# Kółko

Na `/circle-sims` dopisujesz **nazwane kółko** tenanta: kod snake oraz parę UN/LOCODE rozładunek / załadunek (constraint unload A ∩ load B jako dane). To nie silnik ≥500k i nie kalkulator km.

1. Wejdź na Kółko. Wpisz kod (`backhaul_a` — snake 2–32).
2. Podaj UN/LOCODE rozładunku i załadunku (5 znaków, różne końce). Serwis nie resolve `port` i nie liczy przecięcia.
3. Podaj `source_ref` (`fixture://circle-sim/…` albo `tenant:manual`).
4. „Zapisz kółko”. Ten sam kod, ta sama para albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: silnik ≥500k, km ładowny/pusty/dolot, P overlap, lista przewoźników, LLM-VRP, what-if, mapa, suma w przeglądarce. Wzorzec korytarza zostaje na `/lane-patterns`. Marża zostaje na `/charges`.

Nazwy w kodzie: `circle_sim` · `sim_code` · `unload_unlocode` · `load_unlocode` · `source_ref`.
