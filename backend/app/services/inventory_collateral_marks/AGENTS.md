# BC inventory_collateral_mark (BR1.3)

HITL katalog znacznika zabezpieczenia na towarze per tenant. mark_code +
collateral_kind pledge|lien|hold|other + source_ref. Nie FK pozycji. Nie live.

## Dozwolone zależności
- `app.models.inventory_collateral_mark`
- `app.repositories.inventory_collateral_marks`
- `app.domain`

## Zakaz
- import innych BC services (inventory_finance_marks, inventory_position_marks, po_financing_marks, charges, extraction)
- zapis `inventory_finance_mark` / `inventory_position_mark` / `po_financing_mark` / `charge`
- FK pozycji · live zastaw · wartość Decimal
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
