# telematics_connector (V5)

Katalog konektora GPS per tenant. HITL reżim + dostawca. Nie poll. Nie sekrety.

- RLS FORCE. OpenFGA `can_manage_telematics_connectors` = member
- `observation_kind`: `omni_telematic` / `external_api`
- `provider_code`: `gbox` / `ikol` / `flotis` / `wialon` / `other`
- Unique `(organization_id, source_ref)`
- Job: `/telematics-connectors`

Delta: [197.0](../deltas/archived/197.0-telematics-connector.md).
