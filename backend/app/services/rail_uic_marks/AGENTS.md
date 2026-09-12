# BC rail_uic_mark (EXP4.2)

HITL katalog znacznika UIC/CIM/SMGS per tenant. mark_code + rail_kind
uic|cim|smgs|other + source_ref. Nie live rail API. Nie km. Nie mapa.

## Dozwolone zależności
- `app.models.rail_uic_mark`
- `app.repositories.rail_uic_marks`
- `app.domain`

## Zakaz
- import innych BC services (rail_cim_marks, trips, charges, extraction)
- zapis `rail_cim_mark` / `trip` / `charge` / `extraction_draft`
- live rail API / km / mapa / wagon live
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
