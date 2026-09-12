# BC regulatory_radar_mark (EXP2.25)

HITL katalog znacznika regulatory radar per tenant. mark_code + radar_kind
notice|deadline|watch|other + source_ref. Nie scrape urzedow. Nie live feed.

## Dozwolone zaleznosci
- `app.models.regulatory_radar_mark`
- `app.repositories.regulatory_radar_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, filing_scheme_marks)
- zapis `charge` / `extraction_draft` / `filing_scheme_mark`
- scrape urzedow · live feed · deadline SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
