# BC cost_allocation_mark (EXP2.3)

HITL katalog znacznika cost allocation per tenant. mark_code + alloc_kind
direct|abc|shared|other + source_ref. Nie allocation SQL. Nie ABC.

## Dozwolone zależności
- `app.models.cost_allocation_mark`
- `app.repositories.cost_allocation_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices, extraction)
- zapis `charge` / `sales_invoice` / `extraction_draft`
- allocation SQL / ABC engine / druga marża
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
