# BC cargo_cover_mark (EXP2.4)

HITL katalog znacznika cargo cover per tenant. mark_code + cover_kind
cargo|liability|policy|other + source_ref. Nie live insurance. Nie polisa HTTP.

## Dozwolone zależności
- `app.models.cargo_cover_mark`
- `app.repositories.cargo_cover_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices, extraction)
- zapis `charge` / `sales_invoice` / `extraction_draft`
- live insurance / polisa HTTP / druga marża
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
