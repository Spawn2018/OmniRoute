# circle_sim (G2.20)

Katalog kółka per tenant. HITL kod + para UN/LOCODE unload/load. Nie silnik. Nie km.

- RLS FORCE. OpenFGA `can_manage_circle_sims` = member
- `sim_code`: snake 2–32
- `unload_unlocode` / `load_unlocode`: token UN/LOCODE, końce różne
- Unique `(organization_id, sim_code)`, `(organization_id, source_ref)` i para
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/circle-sims`

Delta: [266.0](../deltas/archived/266.0-circle-sim.md).
