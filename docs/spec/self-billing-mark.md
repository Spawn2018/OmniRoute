# self_billing_mark (N14)

HITL katalog znacznika self-billing podwykonawcy per tenant. Nie live. Nie JPK.

## Zakres

- Tabela `self_billing_mark`: organization_id, mark_code, billing_kind (`self`|`subcontractor`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/self-billing-marks`. OpenFGA `can_manage_self_billing_marks`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie FK do party. Nie kwota. Nie JPK.

## Poza zakresem

- Live self-billing / JPK / auto FV
- FK party / sales_invoice
- charge / marża

## Zależności

- tenancy · wzorzec HITL mark
