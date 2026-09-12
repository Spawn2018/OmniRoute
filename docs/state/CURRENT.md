# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **414.0** EXP3.0c HITL `po_sku_mark`

**Etap:** Plaster — **415.0** EXP3.0d (delta zaakceptowana `/noc`, wolno `/plaster`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **415.0** EXP3.0d HITL `po_batch_mark` (PO batch line; bez live EDI) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–415.

**Spec (jedyna na sesję):** [docs/deltas/open/415.0-po-batch-mark.md](../deltas/open/415.0-po-batch-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **413.0** zamknięty (`/noc`) — HITL `po_plant_mark`.
**2026-09-12:** Plaster **414.0** zamknięty (`/noc`) — HITL `po_sku_mark`.
**2026-09-12:** Delta **415.0** zaakceptowana (`/noc`) — wolno `/plaster`.
