# BC ocean_feeder_mark (EXP4.3b)

HITL katalog znacznika feeder/short-sea per tenant. mark_code + feeder_kind
feeder|short_sea|other + source_ref. Nie live feeder. Nie TEU. Nie AIS.

## Dozwolone zależności
- `app.models.ocean_feeder_mark`
- `app.repositories.ocean_feeder_marks`
- `app.domain`

## Zakaz
- import innych BC services (ocean_alliance_marks, charges, extraction)
- zapis `ocean_alliance_mark` / `charge` / `extraction_draft`
- live feeder schedule / TEU / AIS / alliance HTTP
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
