# BC tacho_plan_mark (BR3.3)

HITL katalog znacznika ograniczenia tacho w planie per tenant. mark_code +
constraint_kind plan|window|rest|other + source_ref. Nie live DDD.
Nie solver godzin. Nie tacho_office_mark.

## Dozwolone zaleznosci
- `app.models.tacho_plan_mark`
- `app.repositories.tacho_plan_marks`
- `app.domain`

## Zakaz
- import innych BC services (tacho_office_marks, trips, resources, charges, extraction)
- zapis `tacho_office_mark` / `trip` / `resource` / `charge`
- live tacho / DDD parse / Driver Time Solver / godziny SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `trip` / `resource` / `route_plan_mark`
