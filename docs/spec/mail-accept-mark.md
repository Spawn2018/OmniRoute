# Spec: mail_accept_mark (EXP4.16)

HITL katalog znacznika Accept z maila per tenant.

## Pola

- `mark_code` — snake 2–32
- `accept_kind` — `draft` | `clause` | `accept` | `other`
- `source_ref` — `tenant:manual` albo `fixture://mail-accept-mark/…`

## Poza zakresem

Graph live API · auto-send · kwota
