# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **469.0** BR4.3 — HITL `nac_mark`

**Etap:** Plan — delta **470.0** zaakceptowana (`/noc`). Wolno `/plaster`.

**Noc:** `/noc 7` do **2026-09-14T07:00+02**.

**Następny:** plaster **470.0** HITL `silk_corridor_mark`. Nie live CR Express. Nie FK do `shipment_leg` / `lane_pattern`.

Park: `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live NAC HTTP · live CR Express. Nie zgaduj poza 470.0. Nie otwieraj AI0. Nie startuj leftover Valhalla / live CFS / Expo / Alpega / HubSpot.

**Spec (jedyna na sesję):** [470.0](../deltas/open/470.0.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4**, **443.0–469.0** w kodzie. `data_source` = AI5.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-14:** Plan **470.0** (`/noc`) — HITL `silk_corridor_mark`. Wolno plaster.
**2026-09-13:** Plaster **469.0** zamknięty (`/noc`) — HITL `nac_mark`.
**2026-09-13:** Plaster **468.0** zamknięty (`/noc`) — HITL `lcl_console_mark`.
