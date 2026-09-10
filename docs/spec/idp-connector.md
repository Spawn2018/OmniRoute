# idp_connector (S53)

Katalog konektora IdP per tenant. HITL kod + provider `auth0`. Nie login. Nie live HTTP. Nie sekrety.

- RLS FORCE. OpenFGA `can_manage_idp_connectors` = member
- `connector_code`: snake 2–32
- `provider_code`: `auth0` (jedyny token w 270.0)
- `public_domain`: opcjonalny host (tekst, nie issuer)
- Unique `(organization_id, connector_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/idp-connectors`
- JWT hello (0.12/0.15) zostaje sesją

Delta: [270.0](../deltas/archived/270.0-idp-connector.md).
