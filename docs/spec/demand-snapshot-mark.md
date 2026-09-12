# Spec: demand_snapshot_mark (EXP3.13)

HITL katalog znacznika MQC per tenant.

## Pola

- `mark_code` — snake 2–32
- `snapshot_kind` — `sid` | `batch` | `manual` | `other`
- `source_ref` — `tenant:manual` albo `fixture://demand-snapshot-mark/…`

## Poza zakresem

SID live · live giełda hubu · auto-forecast live · kwota
