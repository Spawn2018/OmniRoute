# automation_bias_mark (AI9.1)

Katalog znacznika mitygacji automation bias per tenant. HITL
confirm / delay / review. Nie przebudowa ui-04. Nie scoring osoby.

- RLS FORCE. OpenFGA `can_manage_automation_bias_marks` = member
- `bias_kind`: `confirm` / `delay` / `review` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/automation-bias-marks`

Delta: [482.0](../deltas/open/482.0.md) (po zamknięciu → archived).
