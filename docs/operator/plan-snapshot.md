# Migawka planu

Na `/plan-snapshots` dopisujesz **wersję planu** tenanta: kod snake, trójkę UUID (zlecenie / przejazd / zasób), która musi już istnieć u tenanta, autora i czas. To nie silnik kółek i nie mapa.

1. Wejdź na Migawka planu. Wpisz kod (`plan_v1` — snake 2–32).
2. Wklej trzy UUID z obiektów, które już są w bazie tego tenanta. Obcy albo zmyślony UUID nie wejdzie.
3. Podaj autora (1–64), czas ISO ze strefą i `source_ref` (`fixture://plan-snapshot/…` albo `tenant:manual`).
4. „Zapisz migawkę”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz. Zmiana = nowy INSERT.

Czego tu nie ma: kółka / `circle_sim`, what-if, TT z actuals, km, live HTTP, CASCADE, UPDATE wiersza, suma w przeglądarce. Marża zostaje na `/charges`.

Nazwy w kodzie: `plan_snapshot` · `snapshot_code` · `shipment_id` · `trip_id` · `resource_id` · `author_label` · `recorded_at` · `source_ref`.
