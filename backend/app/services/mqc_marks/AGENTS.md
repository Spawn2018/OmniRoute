# BC mqc_mark (EXP3.5)

HITL katalog znacznika MQC vs actual per tenant. mark_code + mqc_kind
mqc|actual|gap|other + source_ref. Nie MQC SQL. Nie qty float.

## Dozwolone zaleznosci
- `app.models.mqc_mark`
- `app.repositories.mqc_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, purchase_orders, extraction)
- zapis `charge` / `po_line`
- MQC SQL · qty float · druga marza
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
