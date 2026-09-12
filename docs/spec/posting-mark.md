# Spec: posting_mark (EXP4.9)

HITL katalog znacznika MQC per tenant.

## Pola

- `mark_code` — snake 2–32
- `posting_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://posting-mark/…`

## Poza zakresem

SID live · live giełda hubu · tacho DDD live · kwota
