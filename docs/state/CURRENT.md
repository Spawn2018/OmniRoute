# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **473.0** BR5.2 — rozszerzenie CHECK `exchange_connector`

**Etap:** Plan — kolejka po Fali BR pin **2026-09-08c** (nie zgaduj Q). Zero kodu bez delty.

**Noc:** `/noc 7` do **2026-09-14T07:00+02**.

**Następny:** wskaż Q z [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Kolejka — nie startuj 431.0 ani poza pinem bez człowieka.

Park: `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu BR1.2 · FK PO po BR1.2 · live giełda HTTP. Nie otwieraj AI0. Nie startuj leftover Valhalla / live CFS / Expo / Alpega / HubSpot.

**Spec (jedyna na sesję):** brak — czeka na wskazanie Q

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c** + **Fala AI** + **Fala BR**. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Impersonate ≠ decrypt. `charge.source_ref` **jest** (129.0 / 072) — nie otwieraj plastra AI0. **AI1.0–AI1.4**, **443.0–473.0** w kodzie. `data_source` = AI5.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-14:** Plaster **473.0** zamknięty (`/noc`) — rozszerzenie CHECK `exchange_connector`.
**2026-09-14:** Plan **473.0** (`/noc`) — BR5.2 giełdy katalog konektora.
**2026-09-14:** Plaster **472.0** zamknięty (`/noc`) — HITL `po_financing_mark`.
**2026-09-14:** Plaster **471.0** zamknięty (`/noc`) — HITL `factoring_connector`.
