# M-02 outbox_event — zdarzenie wiadomość zapisana

**Moduł żywy:** M-02  
**Plaster:** **79.0** (zamknięty)  
**Status:** tabela `outbox_event` per tenant. Kind tylko `inbound_message_saved`. Status tylko `pending`. Nie Temporal. Nie konsument.

Delta: [79.0](../deltas/archived/79.0-outbox.md).

## Zakres

- RLS FORCE. OpenFGA `can_manage_outbox_events` = member
- `GET/POST /outbox-events`. Unikat `(organization_id, event_kind, subject_id)`
- API poczty składa zdarzenie po create fixture i ingest Graph
- Ekran `/outbox`: lista + zapis po `subject_id`
- Serwis nie importuje inbound / quotations / extraction

## Poza 79.0

konsument · Temporal · send · IMAP · payload JSON · F9.1
