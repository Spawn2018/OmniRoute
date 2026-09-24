# BC charge_code (M-06)

Katalog typowanych kodów opłat + `source_ref` — nie luźny string, nie `rate_line`, nie `charge`.

## Dozwolone zależności
- `app.models.charge_code`
- `app.repositories.charge_codes`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `rate_line` / `charge`
- liczenie kwot / marży
- CHECK allowlisty WAITING|NO_SHOW|DIVERSION|STAMP
- seed Omni czterech kodów w serwisie
