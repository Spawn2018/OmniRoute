# Spec: sid_import_mark (EXP2.21)

HITL katalog znacznika importu SID per tenant.

## Pola

- `mark_code` — snake 2–32
- `sid_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://sid-import-mark/…`

## Poza zakresem

SID live · SID HTTP · ICS2 live · kwota
