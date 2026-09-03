# BC edi_message (M-39)

Komunikat EDI per tenant, FK do `shipment`. Nie parser, nie live siec, nie kwota.

## Dozwolone zależności
- `app.models.edi_message`
- `app.repositories.edi_messages`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, channel_quotes)
- zapis `shipment` / `quotation` / `charge`
- kwoty / marża / float / parser
- HTTP
