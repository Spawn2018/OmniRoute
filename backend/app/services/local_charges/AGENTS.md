# BC local_charge (P4)

Dopłata lokalna THC/ISPS/seal/amendment per tenant. Decimal. Opcjonalne
`carrier_label` / `service_label` (HITL tekst). Nie warning braków, nie marża.

## Dozwolone zależności
- `app.models.local_charge`
- `app.repositories.local_charges`
- `app.domain`

## Zakaz
- import innych BC services (port_surcharges, channel_quotes, charges, quotations, geography, containers, parties)
- zapis `charge` / `port_surcharge` / `channel_quote` / `container` / `party`
- warning braku dopłaty jako fakt
- FK armator/serwis · float / T-SQL / live HTTP
