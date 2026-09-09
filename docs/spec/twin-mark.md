# twin_mark (W1)

Katalog znacznika rodzaju bliźniaka per tenant. HITL osiem postaci. Nie fizyka. Nie `plan_snapshot`.

- RLS FORCE. OpenFGA `can_manage_twin_marks` = member
- `twin_kind`: `vehicle` / `driver` / `container` / `shipment` / `network` / `plan` / `office` / `cargo`
- Unique `(organization_id, source_ref)`
- Job: `/twin-marks`

Delta: [199.0](../deltas/archived/199.0-twin-mark.md).
