# Spec: copy_ban_mark (EXP4.19)

HITL katalog znacznika zakazu copy claimów per tenant.

## Pola

- `mark_code` — snake 2–32
- `ban_kind` — `eight_min` | `fifteen_k` | `five_hundred_k` | `other`
- `source_ref` — `tenant:manual` albo `fixture://copy-ban-mark/…`

## Poza zakresem

copy claimów do UI · Bayer scrape · kwota
