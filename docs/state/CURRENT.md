# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **425.0** EXP1 HITL `language_code_mark`

**Etap:** Plaster — **426.0** EXP1 (delta zaakceptowana, wolno `/plaster`)

**Noc:** `/noc 10` do 2026-09-13T10:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).

**Następny:** **426.0** EXP1 HITL `haulier_role_mark` (booked|actual|other) — kolejka po cutoff.

Park: Graph live · Expo/EAS · GPS live poll · unwrap umów. Nie zgaduj 71–426.

**Spec (jedyna na sesję):** [docs/deltas/open/426.0-haulier-role-mark.md](../deltas/open/426.0-haulier-role-mark.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-12:** Plaster **424.0** zamknięty (`/noc`) — HITL `payment_terms_mark`.
**2026-09-12:** Plaster **425.0** zamknięty (`/noc`) — HITL `language_code_mark`.
**2026-09-12:** Plan **426.0** — HITL `haulier_role_mark` (bez FK party).
