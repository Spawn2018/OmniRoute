# BC ops_room_mark (BR7.0)

HITL katalog warstwy działającej sali operacyjnej per tenant. mark_code +
layer_kind shift|board|escalation|other + source_ref. Nie N8. Nie widok.

## Dozwolone zależności
- `app.models.ops_room_mark`
- `app.repositories.ops_room_marks`
- `app.domain`

## Zakaz
- import innych BC services (war_room_marks, operational_exceptions, tower_impacts, charges, extraction)
- zapis `war_room_mark` / `operational_exception` / `tower_impact` / `charge`
- N8 · drugi czat · T8 live · widok sklejony
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
