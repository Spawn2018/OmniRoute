# BC spend_mark (CI2)

HITL katalog rodzaju wycieku spend per tenant. mark_code + leakage_kind invoice|clause|other + source_ref. Nie SQL FV vs charge. Nie druga marża.

## Dozwolone zależności
- `app.models.spend_mark`
- `app.repositories.spend_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices, extraction, freight_audit_marks)
- zapis `charge` / `sales_invoice` / `freight_audit_mark`
- SQL FV vs charge / druga marża / float / kwota
- HTTP
- UPDATE / DELETE wiersza
