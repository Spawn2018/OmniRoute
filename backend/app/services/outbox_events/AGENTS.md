# BC outbox_event (M-02)

Zdarzenie między BC per tenant. Pierwszy kind: `inbound_message_saved`. Nie Temporal, nie konsument.

## Dozwolone zależności
- `app.models.outbox_event`
- `app.repositories.outbox_events`
- `app.domain`

## Zakaz
- import innych BC services (inbound, quotations, extraction, mail_drafts)
- worker / dispatcher / Temporal / Hatchet
- HTTP do Graph / IMAP / SMTP
- liczenie kwot / marży
- JSON payload
