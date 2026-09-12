# Spec: inventory_position_mark (EXP3.3)

HITL katalog znacznika Inventory position per tenant.

## Pola

- `mark_code` — snake 2–32
- `stock_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://inventory-position-mark/…`

## Poza zakresem

SID live · live giełda hubu · bilans SQL live · kwota
