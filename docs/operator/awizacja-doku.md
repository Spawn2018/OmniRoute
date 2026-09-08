# Awizacja doku

Na `/dock-appointments` zapisujesz okno TIME na punkcie trasy w magazynie spedycyjnym. To nie WMS i nie awizacja terminalu morskiego.

1. Na `/shipments` zapisz zlecenie i `stop` w miejscu `postal_zone` albo `address` (nie UN/LOCODE).
2. Wejdź na Awizacje doku. Podaj `appointment_code` (snake), status (`noted` / `advised` / `at_dock` / `released`), `stop_id` z tej trasy, dzień i godziny lokalne okna.
3. Koniec okna musi być po starcie. Port UN/LOCODE na stopie odpada — to T8, nie cross-dock. Stop z innego zlecenia odpada jako obca trasa.
4. „Zapisz awizację doku” z `source_ref` (`fixture://dock-appointment/…` albo `tenant:manual`).

Czego tu nie ma: stany magazynowe, drzwi doków, overnight, yard, EIR, kamera, kwota. Marża zostaje na `/charges`.

Nazwy w kodzie: `dock_appointment` · `appointment_code` · `appointment_status` · `window_date` · `window_start_local` · `window_end_local` · `stop_id` · `source_ref`.
