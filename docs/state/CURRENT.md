# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **427.0** EXP1 HITL `diversion_mark`

**Etap:** Plaster — **428.0** EXP1 (delta zaakceptowana, wolno `/plaster`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **428.0** EXP1 HITL `spot_contract_mark` (spot|contract|other) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–428.

**Spec (jedyna na sesję):** [docs/deltas/open/428.0-spot-contract-mark.md](../deltas/open/428.0-spot-contract-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **426.0** zamknięty (`/noc`) — HITL `haulier_role_mark`.
**2026-09-12:** Plaster **427.0** zamknięty (`/noc`) — HITL `diversion_mark`.
**2026-09-12:** Plan **428.0** — HITL `spot_contract_mark` (skip temp — duplikat reefer).
