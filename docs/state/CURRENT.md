# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **426.0** EXP1 HITL `haulier_role_mark`

**Etap:** Plaster — **427.0** EXP1 (delta zaakceptowana, wolno `/plaster`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **427.0** EXP1 HITL `diversion_mark` (diversion|reroute|other) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–427.

**Spec (jedyna na sesję):** [docs/deltas/open/427.0-diversion-mark.md](../deltas/open/427.0-diversion-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **425.0** zamknięty (`/noc`) — HITL `language_code_mark`.
**2026-09-12:** Plaster **426.0** zamknięty (`/noc`) — HITL `haulier_role_mark`.
**2026-09-12:** Plan **427.0** — HITL `diversion_mark` (bez FK shipment).
