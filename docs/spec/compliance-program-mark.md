# compliance_program_mark (AI9.2 leftover)

Katalog znacznika stancji programu zgodności per tenant. HITL
draft / review / signed / exempt. Nie PDF. Nie U-art50.

- RLS FORCE. OpenFGA `can_manage_compliance_program_marks` = member
- `program_kind`: `draft` / `review` / `signed` / `exempt` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/compliance-program-marks`

Delta: [488.0](../deltas/open/488.0.md).
