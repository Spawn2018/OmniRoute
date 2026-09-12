# BC demo_wipe_mark (Demo-1)

HITL katalog znacznika wipe demo per tenant. mark_code + wipe_kind
usun|retain|other + source_ref. Nie live wipe. Nie kasowanie wierszy.

## Dozwolone zależności
- `app.models.demo_wipe_mark`
- `app.repositories.demo_wipe_marks`
- `app.domain`

## Zakaz
- import innych BC services (demo_gps_marks, charges, extraction)
- zapis `demo_gps_mark` / `charge` / `extraction_draft`
- live wipe tenant data / DELETE wierszy biznesowych
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
