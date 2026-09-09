# Bliźniak

Na `/twin-marks` zapisujesz **znacznik rodzaju bliźniaka** tenanta (osiem postaci: pojazd, kierowca, kontener, zlecenie, sieć, plan, urząd, ładunek). To nie silnik fizyki i nie `plan_snapshot`.

1. Wejdź na Bliźniak. Wybierz postać (`vehicle` / `driver` / `container` / `shipment` / `network` / `plan` / `office` / `cargo`).
2. Podaj `source_ref` (`fixture://twin-mark/…` albo `tenant:manual`).
3. „Zapisz bliźniaka”.

Czego tu nie ma: osiem silników symulacji, kółka G2.20, tacho, what-if, suma w przeglądarce. Flota zostaje na `/shipments`. Marża zostaje na `/charges`.

Nazwy w kodzie: `twin_mark` · `twin_kind` · `source_ref`.
