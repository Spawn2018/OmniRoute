# line_impact_layer_mark (BR7.1)

Katalog znacznika warstwy liczonej wpływu na linię per tenant. HITL
scored / forecast / actual. Nie SQL. Nie EBITDA. Nie plant live.

- RLS FORCE. OpenFGA `can_manage_line_impact_layer_marks` = member
- `layer_kind`: `scored` / `forecast` / `actual` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/line-impact-layer-marks`

Delta: [479.0](../deltas/open/479.0.md) (po zamknięciu → archived).
