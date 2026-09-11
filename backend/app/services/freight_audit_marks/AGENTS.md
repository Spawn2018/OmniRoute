# BC freight_audit_mark (CT10)

HITL katalog rodzaju audytu frachtu per tenant. mark_code + audit_kind + source_ref. Nie FV vs charge. Nie druga marża.

## Dozwolone zależności
- `app.models.freight_audit_mark`
- `app.repositories.freight_audit_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices, extraction)
- zapis `charge` / `sales_invoice`
- SQL porównania do charge / druga marża / float / kwota
- HTTP
- UPDATE / DELETE wiersza
