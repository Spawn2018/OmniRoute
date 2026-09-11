# Billing SaaS Omni (G16)

Operator zapisuje katalogowy znacznik billingu: kod, `billing_kind`
(`seat` / `usage` / `invoice` / `other`) i `source_ref`. To dane HITL,
nie live Stripe, nie limity SQL i nie invoice PDF.

Nie liczy kwot. Marża nadal tylko na `charge`.

Ścieżka UI: `/billing-marks`.
