# billing_mark (G16)

HITL katalog znacznika billingu SaaS Omni per tenant. Nie live Stripe. Nie limity SQL.

## Zakres

- Tabela `billing_mark`: organization_id, mark_code, billing_kind (`seat`|`usage`|`invoice`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/billing-marks`. OpenFGA `can_edit`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie FK do idp_connector. Nie kwota. Nie Stripe.

## Poza zakresem

- Live Stripe / Paddle / invoice PDF
- platform_usage_daily SQL / limity
- unwrap umów / impersonate
- charge / marża

## Zależności

- S53 idp_connector (klej poza tym plastrem)
