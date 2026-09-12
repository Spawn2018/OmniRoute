# BC empty_depot_mark (EXP4.6)

HITL katalog znacznika empty/depot/chassis per tenant. mark_code + depot_kind
empty|depot|chassis|other + source_ref. Nie depot live API. Nie scrape.

## Dozwolone zaleznosci
- `app.models.empty_depot_mark`
- `app.repositories.empty_depot_marks`
- `app.domain`

## Zakaz
- import innych BC services (containers, charges, extraction)
- zapis `container` / `charge` / `extraction_draft`
- depot live API · depot scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
