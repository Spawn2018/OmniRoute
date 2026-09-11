# working_capital_mark (EXP2.1)

HITL katalog znacznika working capital per tenant. Nie DSO SQL. Nie druga marża.

## Zakres

- Tabela `working_capital_mark`: organization_id, mark_code, capital_kind (`dso`|`cash_at_risk`|`aging`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/working-capital-marks`. OpenFGA `can_edit`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie kwota. Nie aging SQL.

## Poza zakresem

- DSO / cash-at-risk / aging SQL
- druga marża / EBITDA
- charge / float
- HTTP bank

## Zależności

- F1 sales_invoice / cash_flow (klej poza tym plastrem)
