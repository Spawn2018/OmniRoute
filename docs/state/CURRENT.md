# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **428.0** EXP1 HITL `spot_contract_mark`

**Etap:** Plaster — **429.0** EXP1 (delta zaakceptowana `/noc`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **429.0** EXP1 HITL `bid_decision_mark` (go|no_go|hold|other) — wolno `/plaster`.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–429.

**Spec (jedyna na sesję):** [docs/deltas/open/429.0-bid-decision-mark.md](../deltas/open/429.0-bid-decision-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **426.0** zamknięty (`/noc`) — HITL `haulier_role_mark`.
**2026-09-12:** Plaster **427.0** zamknięty (`/noc`) — HITL `diversion_mark`.
**2026-09-13:** Plaster **428.0** zamknięty (`/noc`) — HITL `spot_contract_mark`.
