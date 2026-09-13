# BC ferry_booking_mark (BR4.0)

HITL katalog znacznika rezerwacji/okna promu per tenant. mark_code +
booking_kind booking|window|sailing|other + source_ref. Nie live bilet.
Nie solver art. 9. Nie ferry_art9_mark.

## Dozwolone zaleznosci
- `app.models.ferry_booking_mark`
- `app.repositories.ferry_booking_marks`
- `app.domain`

## Zakaz
- import innych BC services (ferry_art9_marks, trips, stops, charges, extraction)
- zapis `ferry_art9_mark` / `trip` / `stop` / `charge`
- live rezerwacja / bilet HTTP / solver art. 9
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `trip` / `stop` / `route_plan_mark`
