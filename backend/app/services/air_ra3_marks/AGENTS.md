# BC air_ra3_mark (EXP4.1)

HITL katalog znacznika air RA3/lithium per tenant. mark_code + air_kind
ra3|lithium|known_consignor|other + source_ref. Nie IATA live. Nie scrape.

## Dozwolone zaleznosci
- `app.models.air_ra3_mark`
- `app.repositories.air_ra3_marks`
- `app.domain`

## Zakaz
- import innych BC services (dangerous_goods, charges, extraction)
- zapis `dangerous_good` / `charge` / `extraction_draft`
- IATA live · RA3 scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
