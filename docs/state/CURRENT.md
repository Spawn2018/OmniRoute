# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **419.0** EXP0.3 HITL `slot_guarantee_mark`

**Etap:** Plaster — **420.0** EXP1 (delta zaakceptowana `/noc`; EXP0.4 skipped — dubluje copy_ban)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **420.0** EXP1 HITL `freight_term_mark` (prepaid|collect|third_party|other) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–420.

**Spec (jedyna na sesję):** [docs/deltas/open/420.0-freight-term-mark.md](../deltas/open/420.0-freight-term-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **418.0** zamknięty (`/noc`) — HITL `named_place_mark`.
**2026-09-12:** Plaster **419.0** zamknięty (`/noc`) — HITL `slot_guarantee_mark`.
