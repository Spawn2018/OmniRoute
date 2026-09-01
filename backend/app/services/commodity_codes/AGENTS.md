# BC commodity_code (M-09)

Katalog kodów HS/CN — nie luźna nazwa, nie `quotation`, nie IMDG.

## Dozwolone zależności
- `app.models.commodity_code`
- `app.repositories.commodity_codes`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `rate_line` / `charge`
- liczenie kwot / marży
