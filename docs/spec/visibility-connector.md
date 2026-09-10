# visibility_connector (CT7)

Katalog konektora widoczności per tenant. HITL kod + kind `p44`. Nie live HTTP. Nie sekrety. Nie AIS.

- RLS FORCE. OpenFGA `can_manage_visibility_connectors` = member
- `connector_code`: snake 2–32
- `system_kind`: `p44` (jedyny token w 275.0)
- Unique `(organization_id, connector_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/visibility-connectors`

Delta: [275.0](../deltas/archived/275.0-visibility-connector.md).
