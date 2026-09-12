# BC demo_sim_mark (Demo-1b)

HITL katalog znacznika demo sim per tenant. mark_code + sim_kind
fleet_150|months_10|other + source_ref. Nie live sim. Nie generator 150 aut.

## Dozwolone zależności
- `app.models.demo_sim_mark`
- `app.repositories.demo_sim_marks`
- `app.domain`

## Zakaz
- import innych BC services (demo_wipe_marks, demo_gps_marks, charges, extraction)
- zapis `demo_wipe_mark` / `demo_gps_mark` / `charge` / `extraction_draft`
- live demo_sim / generator 150 pojazdów / GPS live
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
