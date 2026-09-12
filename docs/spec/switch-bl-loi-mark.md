# Spec: switch_bl_loi_mark (EXP3.9)

HITL katalog znacznika MQC per tenant.

## Pola

- `mark_code` — snake 2–32
- `instrument_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://switch-bl-loi-mark/…`

## Poza zakresem

SID live · live giełda hubu · LOI scrape live · kwota
