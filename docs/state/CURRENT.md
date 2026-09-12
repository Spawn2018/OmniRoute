# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **416.0** EXP0.9 HITL `un_segregation_mark`

**Etap:** Plaster — **417.0** EXP0.10 (delta zaakceptowana `/noc`, wolno `/plaster`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **417.0** EXP0.10 HITL `dual_ledger_mark` (dwa ledgery; bez druga marża) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–417.

**Spec (jedyna na sesję):** [docs/deltas/open/417.0-dual-ledger-mark.md](../deltas/open/417.0-dual-ledger-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **416.0** zamknięty (`/noc`) — HITL `un_segregation_mark`.
**2026-09-12:** Delta **417.0** zaakceptowana (`/noc`) — wolno `/plaster`.
