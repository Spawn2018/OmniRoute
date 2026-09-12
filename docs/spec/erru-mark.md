# Spec: erru_mark (EXP4.20)

HITL katalog znacznika sprawdzenia ERRU per tenant.

## Pola

- `mark_code` — snake 2–32
- `check_kind` — `to_verify` | `clear` | `hit` | `other`
- `source_ref` — `tenant:manual` albo `fixture://erru-mark/…`

## Poza zakresem

live ERRU · scrape · scoring osoby · kwota
