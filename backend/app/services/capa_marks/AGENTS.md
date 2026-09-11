# BC capa_mark (CT12)

HITL katalog rodzaju QMS per tenant. mark_code + mark_kind capa|eight_d|recurrence + source_ref. Nie workflow CAPA. Nie scoring.

## Dozwolone zależności
- `app.models.capa_mark`
- `app.repositories.capa_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, shipments, extraction, war_room_marks)
- zapis `charge` / `shipment` / `war_room_mark`
- workflow CAPA / 8D silnik / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
