# rfid_mark (BR1.1)

Katalog znacznika RFID per tenant. HITL czytnik, bramka lub znakowanie. Nie live poll. Nie EPC.

- RLS FORCE. OpenFGA `can_manage_rfid_marks` = member
- `rfid_kind`: `reader` / `gate` / `tag` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/rfid-marks`

Delta: [475.0](../deltas/open/475.0.md).
