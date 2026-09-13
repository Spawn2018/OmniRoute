# NAC i agent nominowany (BR4.3)

Operator zapisuje katalogowy stance: kod, `nac_kind`
(`nac` / `nominated` / `agent` / `other`) i `source_ref`. To dane HITL,
nie live NAC HTTP i nie auto-wysyłka dokumentów.

Nie liczy kwot. Marża nadal tylko na `charge`. Role na zleceniu zostają
w I2 `shipment_stakeholder`; adresat dokumentów w I3 `document_dispatch_rule`.

Ścieżka UI: `/nac-marks`.
