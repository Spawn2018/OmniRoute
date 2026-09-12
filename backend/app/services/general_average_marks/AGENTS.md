# BC general_average_mark (EXP3.11)

HITL katalog znacznika general average per tenant. mark_code + average_kind
ga|contribution|sacrifice|other + source_ref. Nie GA live. Nie GA scrape.

## Dozwolone zaleznosci
- `app.models.general_average_mark`
- `app.repositories.general_average_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, ocean_bills, extraction)
- zapis `charge` / `ocean_bill`
- GA live · GA scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
