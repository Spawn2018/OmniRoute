# ops_room_mark (BR7.0)

Katalog znacznika warstwy działającej sali operacyjnej per tenant. HITL
shift / board / escalation. Nie N8. Nie drugi czat. Nie widok sklejony.

- RLS FORCE. OpenFGA `can_manage_ops_room_marks` = member
- `layer_kind`: `shift` / `board` / `escalation` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/ops-room-marks`

Delta: [478.0](../deltas/open/478.0.md) (po zamknięciu → archived).
