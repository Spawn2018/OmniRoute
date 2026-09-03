# Tracking

Lane wyceny na tablicy to jeszcze nie śledzenie. Zdarzenie powstaje, gdy je **zapiszesz** na `/tracking`, na konkretnym zleceniu.

1. Najpierw zapisz zlecenie na `/shipments`.
2. Wejdź na tracking. Wklej `shipment_id`, rodzaj (`departed`, `arrived` albo `noted`), czas ze strefą (ISO) i `source_ref` (`fixture://tracking/…` albo `tenant:manual`).
3. „Zapisz zdarzenie” wstawia wiersz. Czas podajesz Ty — system nic nie wylicza. Nie ma mapy i nie ma ETA.

Czego tu nie ma: AIS, leaflet, współrzędne, odcinki, auto-zdarzenie przy zapisie zlecenia.

Nazwy w kodzie: `tracking_event` · `event_kind` · `occurred_at`.
