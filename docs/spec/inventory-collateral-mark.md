# inventory_collateral_mark (BR1.3)

Katalog znacznika zabezpieczenia na towarze per tenant. HITL zastaw, hipoteka
przenośna lub hold. Nie FK pozycji. Nie live zastaw. Nie kwota.

- RLS FORCE. OpenFGA `can_manage_inventory_collateral_marks` = member
- `collateral_kind`: `pledge` / `lien` / `hold` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/inventory-collateral-marks`

Delta: [477.0](../deltas/archived/477.0-inventory-collateral-mark.md).
