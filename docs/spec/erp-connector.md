# erp_connector (F9)

Katalog konektora Comarch Optima per tenant. HITL kod + kind `optima`. Nie live SOAP. Nie sekrety.

- RLS FORCE. OpenFGA `can_manage_erp_connectors` = member
- `connector_code`: snake 2–32
- `system_kind`: `optima` (jedyny token w 268.0)
- Unique `(organization_id, connector_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/erp-connectors`

Delta: [268.0](../deltas/archived/268.0-erp-connector.md).
