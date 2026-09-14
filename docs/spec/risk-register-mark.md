# risk_register_mark (AI9.2)

Katalog znacznika stancji rejestru ryzyka per tenant. HITL
open / mitigated / accepted. Nie scoring osoby. Nie L3 silnik.
Nie U-art50 label UI.

- RLS FORCE. OpenFGA `can_manage_risk_register_marks` = member
- `risk_kind`: `open` / `mitigated` / `accepted` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/risk-register-marks`

Delta: [481.0](../deltas/open/481.0.md) (po zamknięciu → archived).
