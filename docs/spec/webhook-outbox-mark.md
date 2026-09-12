# Spec: webhook_outbox_mark (EXP2.23)

HITL katalog znacznika webhook outbox per tenant.

## Pola

- `mark_code` — snake 2–32
- `outbox_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://webhook-outbox-mark/…`

## Poza zakresem

SID live · live webhook hubu · Temporal live · kwota
