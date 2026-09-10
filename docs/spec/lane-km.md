# lane_km (G2.21)

Katalog km ładowny / pusty / dolot per tenant. HITL kod + trzy Decimal. Nie Haversine. Nie trip.

- RLS FORCE. OpenFGA `can_manage_lane_kms` = member
- `km_code`: snake 2–32
- `loaded_km` / `empty_km` / `approach_km`: `Numeric(14,4)`, ≥ 0, `0` legalne
- Unique `(organization_id, km_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- Job: `/lane-kms`

Delta: [267.0](../deltas/archived/267.0-lane-km.md).
