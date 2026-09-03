# Odcinek drogowy

Na `/road` zostaje lista stref i adresów. Osobno zapisujesz odcinek na zleceniu — to noga, nie trasa na mapie.

1. Najpierw zapisz zlecenie na `/shipments` i dwie lokalizacje na `/locations` (`postal_zone` albo `address`). Port (`unlocode`) odrzuca.
2. Wejdź na Transport drogowy. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`).
3. „Zapisz odcinek” wiąże te trzy wskazania. Drugi odcinek `road` na to samo zlecenie odrzuca. Ten sam start i koniec też.
4. Lista pokazuje `leg_kind`, zlecenie i obie lokalizacje. System nie liczy kilometrów ani czasu.

Czego tu nie ma: mapa, GPS, TMS, naczepa, kolej, drobnica, kwota. Marża zostaje na `/charges`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `origin_location_id` · `destination_location_id` · `source_ref`.
