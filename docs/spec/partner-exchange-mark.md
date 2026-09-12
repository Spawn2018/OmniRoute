# Spec: partner_exchange_mark (EXP2.24)

HITL katalog znacznika giełda partnerska per tenant.

## Pola

- `mark_code` — snake 2–32
- `exchange_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://partner-exchange-mark/…`

## Poza zakresem

SID live · live giełda hubu · auto-post live · kwota
