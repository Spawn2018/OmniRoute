# Spec: e_delivery_mark (EXP2.19)

HITL katalog znacznika e-Doręczeń per tenant.

## Pola

- `mark_code` — snake 2–32
- `delivery_kind` — `edor` | `registered` | `receipt` | `other`
- `source_ref` — `tenant:manual` albo `fixture://e-delivery-mark/…`

## Poza zakresem

e-Doręczenia live · PUDO HTTP · bajty · kwota
