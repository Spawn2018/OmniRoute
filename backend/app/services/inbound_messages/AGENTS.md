# BC inbound_message (M-32)

Wiadomość przychodząca per tenant: fixture albo ingest `graph://` + `external_id`. Nie IMAP, nie live HTTP, nie send.

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
