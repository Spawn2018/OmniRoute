# BC network (M-12)

Katalog sieci i stowarzyszeń — kopia per tenant. Nie katalog agentów, nie scraping.

## Dozwolone zależności
- `app.models.network`
- `app.repositories.networks`
- `app.domain`

## Zakaz
- import innych BC services
- `network_member` / scraping portali WCA
- zapis `party` / `quotation` / `charge`
- liczenie kwot / marży
