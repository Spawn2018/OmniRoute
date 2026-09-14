# l3_gate_mark (AI8.2)

Katalog znacznika checklisty bramy przed L3 per tenant. HITL
sot / owner / exception / rollback / blast. Nie silnik L3 write.
Nie mutacja `autonomy_level`.

- RLS FORCE. OpenFGA `can_manage_l3_gate_marks` = member
- `gate_kind`: `sot` / `owner` / `exception` / `rollback` / `blast` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/l3-gate-marks`

Delta: [483.0](../deltas/open/483.0.md) (po zamknięciu → archived).
