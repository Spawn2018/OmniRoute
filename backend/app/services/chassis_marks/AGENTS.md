# BC chassis_mark (EXP4.5b)

HITL katalog znacznika chassis/trailer per tenant. mark_code + chassis_kind
chassis|trailer|other + source_ref. Nie live chassis pool. Nie TEU. Nie yard.

## Dozwolone zależności
- `app.models.chassis_mark`
- `app.repositories.chassis_marks`
- `app.domain`

## Zakaz
- import innych BC services (empty_depot_marks, charges, extraction)
- zapis `empty_depot_mark` / `charge` / `extraction_draft`
- live chassis pool / TEU / yard live / WMS
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
