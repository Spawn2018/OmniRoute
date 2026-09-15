# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **495.0** BR6.0 leftover — HITL `crm_dedup_mark`

**Etap:** Plaster — delta **496.0** zaakceptowana. Komenda `/plaster`.

**Noc:** `/noc 8` do **2026-09-15T08:00+02**.

**Następny:** **496.0** BR6.0 leftover — HITL `crm_link_mark` (`link_kind` lead|party|other; nie FK UUID, nie cold-send)

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu SQL · FK PO · live giełda HTTP · live WMS HTTP · live RFID HTTP · live zastaw · N8 / T8 · SQL line impact / EBITDA · BR2.3/BR6.3 Expo · auto-fix bez owner · Mob Expo · L3 write · silnik porównania stylu · silnik auto-zejścia · HubSpot live · Alpega live · cold-send CRM. Nie otwieraj AI0.

**Spec (jedyna na sesję):** [docs/deltas/open/496.0.md](../deltas/open/496.0.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. **443.0–495.0** w kodzie.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-15:** Delta **496.0** zaakceptowana (`/noc 8`) — wolno plaster.
**2026-09-15:** Plaster **495.0** zamknięty (`/noc 8`) — HITL `crm_dedup_mark`.
**2026-09-15:** Plaster **494.0** zamknięty (`/noc 8`) — HITL `shipper_like_mark`.
