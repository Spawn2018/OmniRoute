# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **477.0** BR1.3 — HITL `inventory_collateral_mark`

**Etap:** Plan — delta **478.0** zaakceptowana (`/noc 20`). Wolno `/plaster`.

**Noc:** `/noc 20` do **2026-09-14T20:00+02**.

**Następny:** **478.0** BR7.0 — HITL `ops_room_mark` (warstwa działająca sali operacyjnej)

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu SQL · FK PO · live giełda HTTP · live WMS HTTP · live RFID HTTP · live zastaw · N8 / T8 live / widok sklejony W2. Nie otwieraj AI0. Nie startuj leftover Valhalla / live CFS / Expo / Alpega / HubSpot.

**Spec (jedyna na sesję):** [ops-room-mark.md](../spec/ops-room-mark.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4**, **443.0–477.0** w kodzie. `data_source` = AI5.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-14:** Plan **478.0** (`/noc 20`) — BR7.0 katalog `ops_room_mark`; delta zaakceptowana.
**2026-09-14:** Plaster **477.0** zamknięty (`/noc 20`) — HITL `inventory_collateral_mark`.
**2026-09-14:** Plan **477.0** (`/noc 20`) — BR1.3 katalog `inventory_collateral_mark`.
**2026-09-14:** Plaster **476.0** zamknięty (`/noc 20`) — HITL `inventory_finance_mark`.
**2026-09-14:** Plan **476.0** (`/noc 20`) — BR1.2 katalog `inventory_finance_mark`.
**2026-09-14:** Plaster **475.0** zamknięty (`/noc 17`) — HITL `rfid_mark`.
