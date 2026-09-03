# BC network (M-12)

Katalog sieci i stowarzyszeń — kopia per tenant. Ręczny `network_member`. Nie scraping.

## Dozwolone zależności
- `app.models.network`
- `app.models.network_member`
- `app.repositories.networks`
- `app.domain`

## Zakaz
- import innych BC services
- scraping portali WCA
- zapis `party` / `quotation` / `charge`
- liczenie kwot / marży
