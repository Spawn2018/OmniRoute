# BC billing_mark (G16)

HITL katalog znacznika billingu SaaS Omni per tenant. mark_code + billing_kind
seat|usage|invoice|other + source_ref. Nie live Stripe. Nie limity SQL.

## Dozwolone zależności
- `app.models.billing_mark`
- `app.repositories.billing_marks`
- `app.domain`

## Zakaz
- import innych BC services (idp_connectors, charges, extraction)
- zapis `idp_connector` / `charge` / `session` / `extraction_draft`
- live Stripe / Paddle / usage SQL / invoice PDF / webhook
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
