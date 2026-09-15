# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **492.0** BR6.1 leftover — `volume_label` tekst na `sales_lane`

**Etap:** Plaster — delta **493.0** zaakceptowana. Komenda `/plaster`.

**Noc:** `/noc 8` do **2026-09-15T08:00+02**.

**Następny:** **493.0** BR6.2 leftover — HITL `shipper_round_mark` (`round_kind` first|second|final|other; nie Alpega)

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu SQL · FK PO · live giełda HTTP · live WMS HTTP · live RFID HTTP · live zastaw · N8 / T8 · SQL line impact / EBITDA · BR2.3/BR6.3 Expo · auto-fix bez owner · Mob Expo · L3 write · silnik porównania stylu · silnik auto-zejścia · HubSpot live. Nie otwieraj AI0.

**Spec (jedyna na sesję):** [docs/deltas/open/493.0.md](../deltas/open/493.0.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. **443.0–492.0** w kodzie.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-15:** Delta **493.0** zaakceptowana (`/noc 8`) — wolno plaster.
**2026-09-15:** Plaster **492.0** zamknięty (`/noc 8`) — `volume_label` na `sales_lane`.
**2026-09-15:** Plaster **491.0** zamknięty (`/noc 8`) — para UN/LOCODE na `sales_lane`.
