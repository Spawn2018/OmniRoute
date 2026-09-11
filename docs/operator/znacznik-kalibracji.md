# Znacznik kalibracji (CI7)

Operator zapisuje katalogowy znacznik gotowości próbki: kod, `sample_ready`
(`ready` / `pending`) i `source_ref`. To dane HITL, nie MAE SQL i nie float.

Nie liczy kalibracji. Nie zapisuje `prediction_ledger`. Marża nadal tylko na `charge`.

Ścieżka UI: `/calibration-marks`.
