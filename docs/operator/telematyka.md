# Konektor GPS

Na `/telematics-connectors` zapisujesz **konektor telematyki** tenanta (reżim obserwacji i kod dostawcy). To nie poll floty i nie ślad pozycji.

1. Wejdź na Konektor GPS. Wybierz reżim (`omni_telematic` / `external_api`) i dostawcę (`gbox` / `ikol` / `flotis` / `wialon` / `other`).
2. Podaj `source_ref` (`fixture://telematics-connector/…` albo `tenant:manual`).
3. „Zapisz konektor GPS”.

Czego tu nie ma: live HTTP GBOX/IKOL, ciphertext, lat/lng, trzy dni robocze, AIS, suma w przeglądarce. Flota zostaje na `/shipments`. Marża zostaje na `/charges`.

Nazwy w kodzie: `telematics_connector` · `observation_kind` · `provider_code` · `source_ref`.
