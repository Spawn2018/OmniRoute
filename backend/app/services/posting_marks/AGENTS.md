# BC posting_mark (EXP4.9)

HITL katalog znacznika posting per tenant. mark_code + posting_kind
posting|delegation|host|other + source_ref. Nie posting live API. Nie tacho DDD.

## Dozwolone zaleznosci
- `app.models.empty_depot_mark`
- `app.repositories.empty_depot_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- posting live API · tacho DDD · prawo per kraj · kwota
- HTTP
- UPDATE / DELETE wiersza
