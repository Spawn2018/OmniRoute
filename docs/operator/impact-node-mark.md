# Wezel skutku (AI6.0)

Operator zapisuje katalogowy znacznik węzła kaskady Business Impact Graph: kod,
`node_kind` (`shipment` / `inventory` / `sku` / `line` / `order` / `revenue` /
`margin` / `cash` / `other`) i `source_ref`. To dane HITL, nie SQL grafu i nie EBITDA.

Nie liczy kwot. Marża nadal tylko na `charge`. `tower_impact` i `impact_scenario` zostają osobno.

Ścieżka UI: `/impact-node-marks`.
