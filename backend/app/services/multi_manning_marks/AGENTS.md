# BC multi_manning_mark (EXP4.8)

HITL katalog znacznika multi-manning per tenant. mark_code + manning_kind
dual|relay|team|other + source_ref. Nie tacho live API. Nie trip.driver2.

## Dozwolone zaleznosci
- `app.models.empty_depot_mark`
- `app.repositories.empty_depot_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, resources, charges, extraction)
- zapis `trip` / `resource` / `charge` / `extraction_draft`
- tacho live API · driver scrape · trip.driver2 · kwota
- HTTP
- UPDATE / DELETE wiersza
