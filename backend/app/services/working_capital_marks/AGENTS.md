# BC working_capital_mark (EXP2.1)

HITL katalog znacznika working capital per tenant. mark_code + capital_kind
dso|cash_at_risk|aging|other + source_ref. Nie DSO SQL. Nie druga marża.

## Dozwolone zależności
- `app.models.working_capital_mark`
- `app.repositories.working_capital_marks`
- `app.domain`

## Zakaz
- import innych BC services (cash_flows, sales_invoices, charges, extraction)
- zapis `cash_flow` / `sales_invoice` / `charge` / `extraction_draft`
- DSO SQL / aging SQL / druga marża / EBITDA
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
