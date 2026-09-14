# Przepływ WMS (BR1.0)

Operator zapisuje katalogowy stance operacji magazynowej: kod, `flow_kind`
(`receipt` / `location` / `pick` / `ship` / `count` / `other`) i `source_ref`.
To dane HITL — nie live WMS, nie ilości, nie RFID ani lokalizacja bin.

Nie liczy kwot. Marża nadal tylko na `charge`. Awizacja doku spedycyjnego
zostaje w `dock_appointment`; pozycja zapasu w `inventory_position_mark`.

Ścieżka UI: `/wms-flow-marks`.
