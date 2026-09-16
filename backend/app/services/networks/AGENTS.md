# BC network (M-12)

Katalog sieci i stowarzyszeń — kopia per tenant. Ręczny `network_member`. Nie scraping.
Lista członków: opcjonalny filtr `country_code` JOIN `party` (O7 / 532.0) — odczyt, nie zapis.

## Dozwolone zależności
- `app.models.network`
- `app.models.network_member`
- `app.models.party` — tylko JOIN odczytu kraju w repozytorium
- `app.repositories.networks`
- `app.domain`

## Zakaz
- import innych BC services
- scraping portali WCA
- zapis `party` / `quotation` / `charge`
- liczenie kwot / marży
- druga kolumna kraju na `network_member`