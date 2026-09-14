# BC inventory_finance_mark (BR1.2)

HITL katalog znacznika zapasu finansowego per tenant. mark_code + finance_kind
valuation|aging|release|other + source_ref. Nie wycena SQL. Nie kwota.

## Dozwolone zależności
- `app.models.inventory_finance_mark`
- `app.repositories.inventory_finance_marks`
- `app.domain`

## Zakaz
- import innych BC services (inventory_position_marks, po_financing_marks, working_capital_marks, charges, extraction)
- zapis `inventory_position_mark` / `po_financing_mark` / `working_capital_mark` / `charge`
- wycena zapasu SQL · wiekowanie SQL · wartość Decimal · live zastaw / SMEO
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
