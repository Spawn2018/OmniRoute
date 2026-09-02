# BC customer_rfq (M-28)

Zapytanie ofertowe per tenant, FK do `inbound_message`. Nie ślad wycen, nie silnik, nie IMAP.

## Dozwolone zależności
- `app.models.customer_rfq`
- `app.repositories.customer_rfqs`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `rate_line` / `charge` / `inbound_message`
- kwoty / marża / float
- HTTP do Graph / IMAP
