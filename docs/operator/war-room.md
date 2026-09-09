# Sala kryzysowa

Na `/war-room-marks` zapisujesz **znacznik rodzaju incydentu** tenanta (pogoda, kongestia, strajk, armator, kredyt, inne). To nie scalanie alertów i nie drugi czat.

1. Wejdź na Sala kryzysowa. Wybierz rodzaj (`weather` / `congestion` / `labor` / `carrier` / `credit` / `other`).
2. Podaj `source_ref` (`fixture://war-room-mark/…` albo `tenant:manual`).
3. „Zapisz salę kryzysową”.

Czego tu nie ma: koalescencja N8, drugi czat, mapa, T8 z API, suma w przeglądarce. Wieża wyjątków zostaje na `/watchtower`. Marża zostaje na `/charges`.

Nazwy w kodzie: `war_room_mark` · `incident_kind` · `source_ref`.
