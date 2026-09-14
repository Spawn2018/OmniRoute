# BC style_cascade_mark (AI8.0)

HITL katalog poziomu kaskady stylu per tenant. mark_code +
cascade_kind global|company|department|user|customer|person|context|other
+ source_ref. Nie STYLE FIDELITY. Nie scoring osoby.

## Dozwolone zależności
- `app.models.style_cascade_mark`
- `app.repositories.style_cascade_marks`
- `app.domain`

## Zakaz
- import innych BC services (twin_marks, charges, extraction, autonomy_levels)
- zapis `twin_mark` / `charge` / `extraction_draft` / `party`
- STYLE FIDELITY SCORE · silnik stylu · scoring osoby · FK party/app_user
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
