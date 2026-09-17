# Self-billing podwykonawcy (N14)

Operator zapisuje katalogowy znacznik self-billing: kod, `billing_kind`
(`self` / `subcontractor` / `other`) i `source_ref`. To dane HITL,
nie live self-billing, nie JPK i nie auto FV.

Nie liczy kwot. Marża nadal tylko na `charge`.

Ścieżka UI: `/self-billing-marks`.
