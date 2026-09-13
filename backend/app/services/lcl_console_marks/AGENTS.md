# BC lcl_console_mark (BR4.2)

HITL katalog stance konsoli LCL/CFS per tenant. mark_code + console_kind
console|cfs|other + source_ref. Nie live CFS. Nie CBM. Nie druga tabela LCL.

## Dozwolone zaleznosci
- `app.models.lcl_console_mark`
- `app.repositories.lcl_console_marks`
- `app.domain`

## Zakaz
- import innych BC services (ocean_bills, shipment_legs, nvocc_marks, charges, extraction)
- zapis `ocean_bill` / `shipment_leg` / `nvocc_mark` / `charge`
- live CFS HTTP / kalkulacja CBM / druga tabela LCL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `ocean_bill` / `shipment_leg` / `nvocc_mark`
