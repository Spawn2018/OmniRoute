# BC self_billing_mark (N14)

HITL katalog znacznika self-billing podwykonawcy per tenant. mark_code +
billing_kind self|subcontractor|other + source_ref. Nie live. Nie JPK.

## Dozwolone zależności
- `app.models.self_billing_mark`
- `app.repositories.self_billing_marks`
- `app.domain`

## Zakaz
- import innych BC services (billing_marks, charges, sales_invoices, extraction)
- zapis `billing_mark` / `charge` / `sales_invoice` / `extraction_draft`
- live self-billing / JPK / auto FV / FK party
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
