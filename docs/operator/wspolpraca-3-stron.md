# Współpraca 3 stron (CT11)

Ekran `/collaboration-marks` zapisuje rolę współpracy jako dane: kod snake, rola `shipper` / `carrier` / `consignee`, oraz `source_ref`.

To katalog HITL. Nie otwiera wspólnego SELECT między tenantami. Nie tworzy tuple OpenFGA na kontrahencie.

Źródło: `tenant:manual` albo `fixture://collaboration-mark/…`.

Czego tu nie ma: portal 3 stron, wspólny odczyt, mapa. Strona zlecenia z `party_id` zostaje na `/shipment-stakeholders`. Marża na `/charges`.
