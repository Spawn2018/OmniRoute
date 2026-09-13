# Przetarg załadowcy (BR6.2)

Operator zapisuje katalogowy tryb: kod, `shipper_kind`
(`round` / `bench` / `spot` / `other`) i `source_ref`. To dane HITL,
nie druga tabela `tender` i nie auto-award.

Nie liczy kwot. Marża nadal tylko na `charge`.
Rundy i like-for-like zostają leftover.

Ścieżka UI: `/shipper-tender-marks`.
