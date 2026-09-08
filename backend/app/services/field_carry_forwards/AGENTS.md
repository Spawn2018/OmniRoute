# BC field_carry_forward (U1)

Snapshot pola z wyceny na zlecenie per tenant. Klucze allowlista. Zmiana = nowy wiersz.
Nie overwrite wyceny. Nie kwota.

## Dozwolone zależności
- `app.models.field_carry_forward`
- `app.repositories.field_carry_forwards`
- `app.domain`

## Zakaz
- import innych BC services (quotations, shipments, charges)
- zapis `quotation` / `shipment` / `charge`
- kwoty / marża / float / dni robocze
- HTTP
