# Krawedz skutku (AI6.0 leftover)

Operator zapisuje katalogowy znacznik krawędzi kaskady Business Impact Graph: kod,
`from_kind` i `to_kind` (te same etykiety co węzeł: `shipment` / `inventory` /
`sku` / `line` / `order` / `revenue` / `margin` / `cash` / `other`) oraz
`source_ref`. To dane HITL — para etykiet, nie FK do `impact_node_mark`, nie SQL
grafu i nie EBITDA.

Nie liczy kwot. Marża nadal tylko na `charge`. `impact_node_mark`, `tower_impact`
i `impact_scenario` zostają osobno.

Ścieżka UI: `/impact-edge-marks`.
