# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **477.0** BR1.3 — HITL `inventory_collateral_mark`

**Etap:** Plan — kolejka po BR1.3 pin **2026-09-08c** (nie zgaduj Q). Zero kodu bez delty.

**Noc:** `/noc 20` do **2026-09-14T20:00+02**.

**Następny:** **BR7.0** sala operacyjna — warstwa działająca — wskaż Q z [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Kolejka

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu SQL · FK PO · live giełda HTTP · live WMS HTTP · live RFID HTTP · live zastaw. Nie otwieraj AI0. Nie startuj leftover Valhalla / live CFS / Expo / Alpega / HubSpot.

**Spec (jedyna na sesję):** brak — czeka na plan BR7.0

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4**, **443.0–477.0** w kodzie. `data_source` = AI5.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-14:** Plaster **477.0** zamknięty (`/noc 20`) — HITL `inventory_collateral_mark`.
**2026-09-14:** Plan **477.0** (`/noc 20`) — BR1.3 katalog `inventory_collateral_mark`.
**2026-09-14:** Plaster **476.0** zamknięty (`/noc 20`) — HITL `inventory_finance_mark`.
**2026-09-14:** Plan **476.0** (`/noc 20`) — BR1.2 katalog `inventory_finance_mark`.
**2026-09-14:** Plaster **475.0** zamknięty (`/noc 17`) — HITL `rfid_mark`.
