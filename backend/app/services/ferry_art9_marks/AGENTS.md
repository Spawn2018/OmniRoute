# BC ferry_art9_mark (EXP2.13)

HITL katalog znacznika ferry art. 9 per tenant. mark_code + ferry_kind
rest|watchdog|crossing|other + source_ref. Nie tacho. Nie Driver Time Solver.

## Dozwolone zależności
- `app.models.ferry_art9_mark`
- `app.repositories.ferry_art9_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, stops, charges, extraction)
- zapis `trip` / `stop` / `charge` / `extraction_draft`
- ferry art. 9 live / tacho DDD / Driver Time Solver / watchdog ETA
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza