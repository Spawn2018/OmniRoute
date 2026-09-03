# BC inbound_message (M-32)

Wiadomość przychodząca per tenant: fixture albo ingest `graph://` / skrzynka + `external_id`. Nie live skrzynka, nie send.

## Dozwolone zależności
- `app.models.inbound_message`
- `app.repositories.inbound_messages`
- `app.domain`

## Zakaz
- import innych BC services
- HTTP do Graph / IMAP / SMTP
- zapis `party` / `quotation` / `rate_line` / `charge`
- wołać ExtractionService / zapis extraction_draft (API składa)
- liczenie kwot / marży
