# BC schedule_exception_mark (EXP2.7)

HITL katalog wyjątku harmonogramu per tenant. mark_code + exception_kind
delay|cancel|reroute|other + source_ref. Nie silnik schedule. Nie ETA.

## Dozwolone zależności
- `app.models.schedule_exception_mark`
- `app.repositories.schedule_exception_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, stops, charges, extraction)
- zapis `trip` / `stop` / `charge` / `extraction_draft`
- live schedule engine / ETA SQL
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
