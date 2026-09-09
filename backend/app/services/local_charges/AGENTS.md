# BC local_charge (P4)

Dopłata lokalna THC/ISPS/seal/amendment per tenant. Decimal. Nie warning braków, nie marża.

## Dozwolone zależności
- `app.models.local_charge`
- `app.repositories.local_charges`
- `app.domain`

## Zakaz
- import innych BC services (port_surcharges, channel_quotes, charges, quotations, geography, containers)
- zapis `charge` / `port_surcharge` / `channel_quote` / `container`
- warning braku dopłaty jako fakt
- float / T-SQL / live HTTP
