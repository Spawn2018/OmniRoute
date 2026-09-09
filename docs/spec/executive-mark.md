# executive_mark (W4)

Katalog znacznika pytania zarządu per tenant. HITL rodzaj. Nie suma LLM. Nie zdania z agregatów SQL.

- RLS FORCE. OpenFGA `can_manage_executive_marks` = member
- `question_kind`: `loss` / `lane` / `risk` / `cash` / `other`
- Unique `(organization_id, source_ref)`
- Job: `/executive-marks`

Delta: [202.0](../deltas/archived/202.0-executive-mark.md).
