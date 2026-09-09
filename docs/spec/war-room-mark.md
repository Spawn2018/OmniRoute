# war_room_mark (W2)

Katalog znacznika incydentu sali per tenant. HITL rodzaj. Nie koalescencja N8. Nie drugi czat.

- RLS FORCE. OpenFGA `can_manage_war_room_marks` = member
- `incident_kind`: `weather` / `congestion` / `labor` / `carrier` / `credit` / `other`
- Unique `(organization_id, source_ref)`
- Job: `/war-room-marks`

Delta: [200.0](../deltas/archived/200.0-war-room-mark.md).
