# plan_snapshot (B0b)

Katalog wersji planu per tenant. HITL trójka UUID jako dane. Nie silnik. Nie kółka.

- RLS FORCE. OpenFGA `can_manage_plan_snapshots` = member
- `snapshot_code`: snake 2–32
- `shipment_id` / `trip_id` / `resource_id`: UUID bez FK
- `author_label` 1–64; `recorded_at` timestamptz HITL
- Unique `(organization_id, snapshot_code)` i `(organization_id, source_ref)`
- Append-only INSERT
- Job: `/plan-snapshots`

Delta: [265.0](../deltas/archived/265.0-plan-snapshot.md).
