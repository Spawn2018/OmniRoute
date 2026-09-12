# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **420.0** EXP1 HITL `freight_term_mark`

**Etap:** Plaster — **421.0** EXP1 (delta zaakceptowana `/noc`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **421.0** EXP1 HITL `customer_po_mark` (customer_po|release|call_off|other) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–421.

**Spec (jedyna na sesję):** [docs/deltas/open/421.0-customer-po-mark.md](../deltas/open/421.0-customer-po-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **419.0** zamknięty (`/noc`) — HITL `slot_guarantee_mark`.
**2026-09-12:** Plaster **420.0** zamknięty (`/noc`) — HITL `freight_term_mark`.
