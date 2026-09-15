# field_confidence_mark (AI9.1 leftover)

Katalog znacznika pasma pewności per pole (ui-04) per tenant. HITL
green / yellow / orange / hold. Nie przebudowa splitu. Nie float.

- RLS FORCE. OpenFGA `can_manage_field_confidence_marks` = member
- `band_kind`: `green` / `yellow` / `orange` / `hold` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/field-confidence-marks`

Delta: [487.0](../deltas/archived/487.0-field-confidence-mark.md).
