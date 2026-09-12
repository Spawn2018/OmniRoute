# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **377.0** EXP3.12 HITL `tender_decline_reason`

**Etap:** Plan — **378.0** EXP3.13

**Noc:** `/noc 10` do 2026-09-12T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **378.0** EXP3.13 demand_snapshot HITL `demand_snapshot_mark`.

Park: demand SQL · 3-way OpenFGA · CAPA (istnieje `capa_mark`?). Nie zgaduj 71–378.

**Spec (jedyna na sesję):** (brak — plan 378.0).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **377.0** zamknięty (`/noc`) — HITL `tender_decline_reason` (OTIF split pominięty).
