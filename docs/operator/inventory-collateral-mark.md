# Zabezpieczenie na towarze (BR1.3)

Operator zapisuje katalogowy stance zabezpieczenia na towarze: kod,
`collateral_kind` (`pledge` / `lien` / `hold` / `other`) i `source_ref`.
To dane HITL — nie powiązanie z konkretną pozycją magazynową ani live zastaw.

Nie liczy kwot. Marża nadal tylko na `charge`. Pozycja WMS zostaje w
`inventory_position_mark`; zapas finansowy w `inventory_finance_mark`.

Ścieżka UI: `/inventory-collateral-marks`.
