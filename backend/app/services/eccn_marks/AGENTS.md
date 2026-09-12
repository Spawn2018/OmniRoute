# BC eccn_mark (EXP3.6)

HITL katalog znacznika ECCN per tenant. mark_code + control_kind
eccn|ear|license|other + source_ref. Nie ECCN live. Nie license HTTP.

## Dozwolone zaleznosci
- `app.models.eccn_mark`
- `app.repositories.eccn_marks`
- `app.domain`

## Zakaz
- import innych BC services (commodity_codes, charges, extraction)
- zapis `commodity_code` / `charge`
- ECCN live · license HTTP · qty float
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
