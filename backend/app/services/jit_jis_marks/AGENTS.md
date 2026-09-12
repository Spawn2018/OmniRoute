# BC jit_jis_mark (EXP3.1)

HITL katalog znacznika JIT/JIS per tenant. mark_code + flow_kind
jit|jis|kanban|other + source_ref. Nie WMS live. Nie silnik JIT.

## Dozwolone zaleznosci
- `app.models.jit_jis_mark`
- `app.repositories.jit_jis_marks`
- `app.domain`

## Zakaz
- import innych BC services (purchase_orders, charges, extraction)
- zapis `purchase_order` / `po_line` / `asn` / `charge`
- WMS live · silnik JIT · inventory SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
