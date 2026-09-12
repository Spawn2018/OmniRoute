# BC ocean_alliance_mark (EXP4.3)

HITL katalog znacznika ocean alliance/feeder per tenant. mark_code + ocean_kind
alliance|feeder|slot|other + source_ref. Nie ocean live API. Nie scrape.

## Dozwolone zaleznosci
- `app.models.ocean_alliance_mark`
- `app.repositories.ocean_alliance_marks`
- `app.domain`

## Zakaz
- import innych BC services (ocean_bills, charges, extraction)
- zapis `ocean_bill` / `charge` / `extraction_draft`
- ocean live API · alliance scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
