# memory_edge (W3)

Katalog znacznika krawędzi pamięci per tenant. HITL rodzaj. Nie graf na `entity_event`. Nie wyszukiwanie stawek.

- RLS FORCE. OpenFGA `can_manage_memory_edges` = member
- `edge_kind`: `recalls` / `follows` / `blocks` / `cites` / `other`
- Unique `(organization_id, source_ref)`
- Job: `/memory-edges`

Delta: [201.0](../deltas/archived/201.0-memory-edge.md).
