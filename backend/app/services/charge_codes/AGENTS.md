# BC charge_code (M-06)

Katalog typowanych kodów opłat — nie luźny string, nie `rate_line`, nie `charge`.

## Dozwolone zależności
- `app.models.charge_code`
- `app.repositories.charge_codes`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `rate_line` / `charge`
- liczenie kwot / marży
