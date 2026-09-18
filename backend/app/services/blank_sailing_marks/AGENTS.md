# BC blank_sailing_mark (V3)

HITL katalog znacznika blank sailing per tenant. mark_code + sailing_kind
blank|congestion|gate|other + source_ref. Nie countdown N3. Nie szkic charge.

## Dozwolone zależności
- `app.models.blank_sailing_mark`
- `app.repositories.blank_sailing_marks`
- `app.domain`

## Zakaz
- import innych BC services (free_time_clocks, schedule_exception_marks, charges, extraction)
- zapis `free_time_clock` / `schedule_exception_mark` / `charge` / `container`
- countdown N3 / predykcja blank sailing / live armator
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
