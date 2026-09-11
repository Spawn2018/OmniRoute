# Egzekucja przewodnika (CT4 leftover)

Ekran `/routing-guide-enforcements` zapisuje tryb egzekucji jako dane: kod snake, rodzaj `record_only` albo `block_409`, oraz `source_ref`.

To katalog HITL. Nie blokuje zlecenia HTTP 409 w tym plasterze. Nie dopasowuje trasy w Pythonie.

Źródło: `tenant:manual` albo `fixture://routing-guide-enforcement/…`.

Czego tu nie ma: żywy 409 na POST shipment/ASN, matching guide vs trasa, mapa. Sam przewodnik zostaje na `/routing-guides`. Marża na `/charges`.
