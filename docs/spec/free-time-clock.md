# free_time_clock (V3)

Katalog zegara D&D/rollover per tenant. HITL rodzaj + dni wolne. Nie countdown. Nie szkic `charge`.

- RLS FORCE. OpenFGA `can_manage_free_time_clocks` = member
- `clock_kind`: `demurrage` / `detention` / `mixed` / `rollover`
- `free_days`: integer ≥ 0, dana, nie `now() − gate_in`
- Unique `(organization_id, source_ref)`
- Job: `/free-time-clocks`

Delta: [196.0](../deltas/archived/196.0-free-time-clock.md).
