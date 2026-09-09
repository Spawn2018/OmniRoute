# tower_impact (V6)

Katalog znacznika łańcucha wieży per tenant. HITL etap + status umowy. Nie silnik EBITDA. Nie scoring osoby.

- RLS FORCE. OpenFGA `can_manage_tower_impacts` = member
- `chain_stage`: `stock` / `production` / `sales` / `ebitda`
- `contract_data_status`: `missing` / `recorded` (`missing` → „brak danych umowy”)
- Unique `(organization_id, source_ref)`
- Job: `/tower-impacts`

Delta: [198.0](../deltas/archived/198.0-tower-impact.md).
