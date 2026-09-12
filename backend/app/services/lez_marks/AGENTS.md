# BC lez_mark (EXP4.11)

HITL katalog znacznika LEZ/zakazy per tenant. mark_code + lez_kind
lez|ban|zone|other + source_ref. Nie LEZ live API. Nie mapa zakazow.

## Dozwolone zaleznosci
- `app.models.empty_depot_mark`
- `app.repositories.empty_depot_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- LEZ live API · mapa zakazow · GPS geofence · kwota
- HTTP
- UPDATE / DELETE wiersza
