# exchange_connector (S55)

Katalog konektora giełdy per tenant. HITL kod + kind `trans_eu`. Nie live HTTP. Nie sekrety. Nie SPA.

- RLS FORCE. OpenFGA `can_manage_exchange_connectors` = member
- `connector_code`: snake 2–32
- `system_kind`: `trans_eu` (jedyny token w 271.0)
- Unique `(organization_id, connector_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/exchange-connectors`

Delta: [271.0](../deltas/archived/271.0-exchange-connector.md).
