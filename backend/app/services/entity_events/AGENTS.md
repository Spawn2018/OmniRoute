# BC entity_event (B0a)

Ledger zdarzeń podmiotu per tenant. Append-only INSERT. Nie outbox, nie predykcja, nie Temporal.

## Dozwolone zależności
- `app.models.entity_event`
- `app.repositories.entity_events`
- `app.domain`

## Zakaz
- import innych BC services (quotations, carrier_inquiries, channel_quotes, outbox_events)
- zapis `quotation` / `carrier_inquiry` / `channel_quote` / `outbox_event`
- UPDATE / DELETE wiersza
- JSON payload / kwoty / marża / float
- HTTP / Temporal / worker
