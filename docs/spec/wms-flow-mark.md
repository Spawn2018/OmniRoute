# wms_flow_mark (BR1.0)

Katalog znacznika przepływu WMS per tenant. HITL rodzaj operacji magazynowej. Nie live WMS. Nie qty.

- RLS FORCE. OpenFGA `can_manage_wms_flow_marks` = member
- `flow_kind`: `receipt` / `location` / `pick` / `ship` / `count` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/wms-flow-marks`

Delta: [474.0](../deltas/open/474.0.md).
