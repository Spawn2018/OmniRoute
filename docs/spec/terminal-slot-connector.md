# terminal_slot_connector (T8)

Katalog capability slotu per tenant. HITL kod + terminal jako dana + `mode` + godziny N4. Nie booking. Nie live T8.

- RLS FORCE. OpenFGA `can_manage_terminal_slot_connectors` = member
- `connector_code` / `terminal_code`: snake 2–32
- `mode`: `api` / `email_hitl` / `portal_task` / `unsupported`
- `opens_local` / `closes_local` / `cutoff_local`: TIME, wpis operatora
- Unique `(organization_id, connector_code)`, `(organization_id, terminal_code)` i `(organization_id, source_ref)`
- Kolumna `confirmed` nie istnieje; Create `extra=forbid`
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/terminal-slot-connectors`

Delta: [269.0](../deltas/archived/269.0-terminal-slot-connector.md).
