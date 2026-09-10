# entity_event (B0a)

Ledger zdarzeń podmiotu per tenant. Append-only INSERT. Nie outbox, nie `prediction_ledger`.

- RLS FORCE. OpenFGA `can_manage_entity_events` = member
- `event_kind`: `inquiry_queued` / `inquiry_sent` / `quote_recorded`
- `subject_kind`: `carrier_inquiry` / `quotation` / `channel_quote`
- `source_ref` obowiązkowe. Wskazanie UUID bez FK do innych BC.
- Job: `/entity-events`. POST zapytania `answered` składa `quote_recorded` w API (246.0).
