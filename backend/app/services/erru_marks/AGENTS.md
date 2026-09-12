# BC erru_mark (EXP4.20)

HITL katalog znacznika sprawdzenia ERRU per tenant. mark_code + check_kind
to_verify|clear|hit|other + source_ref. Nie live ERRU. Nie scrape.

## Dozwolone zależności
- `app.models.erru_mark`
- `app.repositories.erru_marks`
- `app.domain`

## Zakaz
- import innych BC services (parties, registry_poll_marks, charges, extraction)
- zapis `party` / `registry_poll_mark` / `charge` / `extraction_draft`
- live ERRU / Citizen API / scrape / scoring osoby / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
