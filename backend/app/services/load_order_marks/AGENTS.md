# BC load_order_mark (BR3.1)

HITL katalog znacznika kolejności załadunku per tenant. mark_code +
order_kind sequence|stack|door|other + source_ref. Nie solver OR.
Nie wymiary Decimal. Nie load_plan_mark.

## Dozwolone zaleznosci
- `app.models.load_order_mark`
- `app.repositories.load_order_marks`
- `app.domain`

## Zakaz
- import innych BC services (load_plan_marks, bin_pack_marks, oog_marks, charges, extraction)
- zapis `load_plan_mark` / `bin_pack_mark` / `oog_mark` / `charge`
- solver OR / LLM-VRP / wymiary Decimal / osie Decimal
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `load_plan_mark` / `trip` / `shipment` / `resource`
