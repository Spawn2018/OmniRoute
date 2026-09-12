# BC demo_gps_mark (EXP0.11)

HITL katalog znacznika demo GPS per tenant. mark_code + demo_kind
seven_day|fleet_demo|other + source_ref. Nie live GPS. Nie lat/lng.

## Dozwolone zależności
- `app.models.demo_gps_mark`
- `app.repositories.demo_gps_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, resources, charges, extraction)
- zapis `trip` / `resource` / `charge` / `extraction_draft`
- live GPS / lat/lng / HTTP poll / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
