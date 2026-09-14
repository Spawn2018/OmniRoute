# style_fidelity_mark (AI8.1)

Katalog stancji bramki fidelity per tenant. HITL
pass / hold / reject / exempt. Nie wyliczanie SCORE. Nie scoring osoby.

- RLS FORCE. OpenFGA `can_manage_style_fidelity_marks` = member
- `fidelity_kind`: `pass` / `hold` / `reject` / `exempt` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/style-fidelity-marks`

Delta: [485.0](../deltas/archived/485.0-style-fidelity-mark.md).
