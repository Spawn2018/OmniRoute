# BC tacho_office_mark (EXP4.10)

HITL katalog znacznika tacho office per tenant. mark_code + tacho_kind
office|card|ddd|other + source_ref. Nie tacho live API. Nie DDD parse.

## Dozwolone zaleznosci
- `app.models.empty_depot_mark`
- `app.repositories.empty_depot_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- tacho live API · DDD parse · prawo per kraj · kwota
- HTTP
- UPDATE / DELETE wiersza
