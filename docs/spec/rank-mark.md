# rank_mark (W5)

Katalog znacznika osi rankingu zakupu per tenant. HITL rodzaj. Nie auto-award. Nie N szkiców.

- RLS FORCE. OpenFGA `can_manage_rank_marks` = member
- `rank_kind`: `price` / `transit` / `reliability` / `carbon` / `other`
- Unique `(organization_id, source_ref)`
- Job: `/rank-marks`

Delta: [203.0](../deltas/archived/203.0-rank-mark.md).
