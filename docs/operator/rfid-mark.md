# RFID magazyn (BR1.1)

Operator zapisuje katalogowy stance identyfikacji automatycznej: kod, `rfid_kind`
(`reader` / `gate` / `tag` / `other`) i `source_ref`. To dane HITL — nie live poll
RFID, nie odczyt EPC ani parowanie z lokalizacją bin.

Nie liczy kwot. Marża nadal tylko na `charge`. Przepływ operacji WMS zostaje
w `wms_flow_mark`; skan paczki Omni w `shipment_package`.

Ścieżka UI: `/rfid-marks`.
