# BC groupage_line (D1)

Katalog linii drobnicy per tenant: cutoff, transit_days, ISODOW, dwa `location`.
Nie WMS. Nie OR hubów. Nie `channel_quote`.

## Dozwolone zależności
- `app.models.groupage_line`
- `app.repositories.groupage_lines`
- `app.domain`

## Zakaz
- import innych BC services (geography, shipments, charges, channel_quotes)
- zapis `location` / `shipment` / `channel_quote` / `charge`
- kwoty / marża / float / WMS
- HTTP / optymalizator
