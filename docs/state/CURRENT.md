# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **475.0** BR1.1 — HITL `rfid_mark`

**Etap:** Plaster — delta **476.0** zaakceptowana (`/noc 20`). Wolno `/plaster`.

**Noc:** `/noc 20` do **2026-09-14T20:00+02**.

**Następny:** **476.0** BR1.2 — HITL `inventory_finance_mark` (wycena|aging|release|other)

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu SQL (leftover po 476.0) · FK PO po BR1.2 · live giełda HTTP · live WMS HTTP · live RFID HTTP. Nie otwieraj AI0. Nie startuj leftover Valhalla / live CFS / Expo / Alpega / HubSpot.

**Spec (jedyna na sesję):** [inventory-finance-mark.md](../spec/inventory-finance-mark.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4**, **443.0–475.0** w kodzie. `data_source` = AI5.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-14:** Plan **476.0** (`/noc 20`) — BR1.2 katalog `inventory_finance_mark`.
**2026-09-14:** Plaster **475.0** zamknięty (`/noc 17`) — HITL `rfid_mark`.
**2026-09-14:** Plan **475.0** (`/noc 17`) — BR1.1 RFID katalog `rfid_mark`.
**2026-09-14:** Plaster **474.0** zamknięty (`/noc 17`) — HITL `wms_flow_mark`.
**2026-09-14:** Plan **474.0** (`/noc 17`) — BR1.0 WMS katalog `wms_flow_mark`.
**2026-09-14:** Plaster **473.0** zamknięty (`/noc`) — rozszerzenie CHECK `exchange_connector`.
