# inventory_finance_mark (BR1.2)

Katalog znacznika zapasu jako obiektu finansowego per tenant. HITL wycena,
wiekowanie lub Inventory Release. Nie silnik wyceny. Nie SQL aging. Nie kwota.

- RLS FORCE. OpenFGA `can_manage_inventory_finance_marks` = member
- `finance_kind`: `valuation` / `aging` / `release` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/inventory-finance-marks`

Delta: [476.0](../deltas/open/476.0.md).
