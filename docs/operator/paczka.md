# Paczka na zleceniu

Na `/shipment-packages` zapisujesz sztukę na zleceniu, nie magazyn i nie linię katalogu.

1. Na `/shipments` zapisz zlecenie, na tym samym ekranie punkt `stop` (kolejność, strefa IANA, miejsce ze słownika).
2. Wejdź na Paczki. Podaj `package_code` (snake), status poziomu paczki (`noted` / `at_stop` / `in_transit` / `delivered`), `stop_id` z tej trasy i token skanu.
3. Token to `omni://shipment-package/{kod}` albo `fixture://omni-qr/{kod}`. Inny kod kreskowy system odrzuca — nie podpina zlecenia z EAN.
4. „Zapisz skan paczki” z `source_ref` (`fixture://shipment-package/…` albo `tenant:manual`). Stop z innego zlecenia odpada jako obca trasa.

Czego tu nie ma: kamera, WMS, `shipment_ref`, etykieta sieci, auto-link bez QR Omni. Marża zostaje na `/charges`.

Nazwy w kodzie: `shipment_package` · `package_code` · `package_status` · `scan_token` · `stop_id` · `source_ref`.
