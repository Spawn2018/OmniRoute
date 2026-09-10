# Km ładowny

Na `/lane-kms` dopisujesz **nazwane km korytarza** tenanta: kod snake oraz trzy odległości wpisane przez operatora — ładowny, pusty i dolot. To nie Haversine, nie mapa i nie suma kółek.

1. Wejdź na Km ładowny. Wpisz kod (`backhaul_a` — snake 2–32).
2. Podaj km ładowny, pusty i dolot jako liczbę dziesiętną (≥ 0; zero jest legalne). Serwis nie liczy z GPS i nie sumuje `/circle-sims`.
3. Podaj `source_ref` (`fixture://lane-km/…` albo `tenant:manual`).
4. „Zapisz km korytarza”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: Haversine, mapa, GPS, suma `circle_sim`, P overlap, lista przewoźników, LLM-VRP, myto, paliwo, kolumny na `trip`. Km przejazdu plan/actual zostaje na `/shipments`. Kółko zostaje na `/circle-sims`. Marża zostaje na `/charges`.

Nazwy w kodzie: `lane_km` · `km_code` · `loaded_km` · `empty_km` · `approach_km` · `source_ref`.
