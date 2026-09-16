# Paczka

Na `/shipment-packages` zapisujesz sztukę na zleceniu, nie magazyn i nie linię katalogu.

1. Weź `shipment_id` i `stop_id` z tej samej trasy.
2. Kod paczki: snake 2–32. Status: `noted` / `at_stop` / `in_transit` / `delivered`.
3. Token to `omni://shipment-package/{kod}` albo `fixture://omni-qr/{kod}`. Inny kod kreskowy system odrzuca — nie podpina zlecenia z EAN.
4. Opcjonalnie `consignment_id` — przesyłka z tego samego zlecenia. Obca przesyłka odpada.
5. „Zapisz skan paczki” z `source_ref` (`fixture://shipment-package/…` albo `tenant:manual`). Stop z innego zlecenia odpada jako obca trasa.

Czego tu nie ma: WMS, kamera, auto-link bez QR Omni, required FK do przesyłki.

Nazwy w kodzie: `shipment_package` · `package_code` · `package_status` · `scan_token` · `stop_id` · `consignment_id` · `source_ref`.
