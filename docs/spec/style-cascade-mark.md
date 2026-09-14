# style_cascade_mark (AI8.0)

Katalog poziomu kaskady stylu per tenant. HITL
global / company / department / user / customer / person / context.
Nie STYLE FIDELITY SCORE. Nie scoring osoby.

- RLS FORCE. OpenFGA `can_manage_style_cascade_marks` = member
- `cascade_kind`: `global` / `company` / `department` / `user` /
  `customer` / `person` / `context` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/style-cascade-marks`

Delta: [484.0](../deltas/archived/484.0-style-cascade-mark.md).
