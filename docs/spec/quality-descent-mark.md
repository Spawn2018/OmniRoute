# quality_descent_mark (AI8.2 leftover)

Katalog powodu zejścia jakości per tenant. HITL
mae / crps / brier / manual. Nie silnik auto-zejścia. Nie L3 write.

- RLS FORCE. OpenFGA `can_manage_quality_descent_marks` = member
- `descent_kind`: `mae` / `crps` / `brier` / `manual` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/quality-descent-marks`

Delta: [486.0](../deltas/archived/486.0-quality-descent-mark.md).
