# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **475.0** BR1.1 — HITL `rfid_mark`

**Etap:** Plan — kolejka po BR1.1 pin **2026-09-08c** (nie zgaduj Q). Zero kodu bez delty.

**Noc:** `/noc 17` do **2026-09-14T17:00+02**.

**Następny:** **BR1.2** zapas jako obiekt finansowy — wskaż Q z [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Kolejka

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu BR1.2 · FK PO po BR1.2 · live giełda HTTP · live WMS HTTP · live RFID HTTP. Nie otwieraj AI0. Nie startuj leftover Valhalla / live CFS / Expo / Alpega / HubSpot.

**Spec (jedyna na sesję):** brak — czeka na plan BR1.2

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4**, **443.0–475.0** w kodzie. `data_source` = AI5.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-14:** Plaster **475.0** zamknięty (`/noc 17`) — HITL `rfid_mark`.
**2026-09-14:** Plan **475.0** (`/noc 17`) — BR1.1 RFID katalog `rfid_mark`.
**2026-09-14:** Plaster **474.0** zamknięty (`/noc 17`) — HITL `wms_flow_mark`.
**2026-09-14:** Plan **474.0** (`/noc 17`) — BR1.0 WMS katalog `wms_flow_mark`.
**2026-09-14:** Plaster **473.0** zamknięty (`/noc`) — rozszerzenie CHECK `exchange_connector`.
