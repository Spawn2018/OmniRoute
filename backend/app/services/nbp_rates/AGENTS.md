# BC nbp_rate (M-23)

Katalog kursu średniego tabeli A NBP — nie `rate_line`, nie przeliczenie wyceny.

## Dozwolone zależności
- `app.models.nbp_rate`
- `app.repositories.nbp_rates`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `rate_line` / `charge`
- liczenie kwot / marży / przeliczeń
