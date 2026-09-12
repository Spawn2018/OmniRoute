# Spec: job_metric_mark (EXP4.21 / M-72)

HITL katalog znacznika metryki jobu per tenant.

## Pola

- `mark_code` — snake 2–32
- `metric_kind` — `time_to_fix` | `touches` | `rework` | `other`
- `source_ref` — `tenant:manual` albo `fixture://job-metric-mark/…`

## Poza zakresem

scoring osoby · SQL job engine · kwota
