# BC ab_sus_mark (EXP4.13)

HITL katalog znacznika A/B+SUS per tenant. mark_code + trial_kind
ab|sus|cohort|other + source_ref. Nie A/B live. Nie scoring SUS.

## Dozwolone zaleznosci
- `app.models.ab_sus_mark`
- `app.repositories.ab_sus_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- A/B live API · scoring SUS · survey live · kwota
- HTTP
- UPDATE / DELETE wiersza
