# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **499.0** BR6.2 leftover — HITL `shipper_award_mark`

**Etap:** Plaster — delta **500.0** zaakceptowana (`/noc 8`). Wolno `/plaster`.

**Noc:** `/noc 8` do **2026-09-15T08:00+02**.

**Następny:** **500.0** AI3.0 leftover — PATCH `candidates` na `quotation` / `customer_rfq` (nie live vision; nie próg 70%)

**Park:** `data_source` (licencja, AI5) · Graph live · Expo/EAS · GPS live poll · unwrap umów · live SMEO HTTP · wycena zapasu SQL · FK PO · live giełda HTTP · live WMS HTTP · live RFID HTTP · live zastaw · N8 / T8 · SQL line impact / EBITDA · BR2.3/BR6.3 Expo · auto-fix bez owner · Mob Expo · L3 write · silnik porównania stylu · silnik auto-zejścia · HubSpot live · Alpega live · cold-send CRM · auto-award SQL. Nie otwieraj AI0.

**Spec (jedyna na sesję):** [docs/deltas/open/500.0.md](../deltas/open/500.0.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan. Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. **443.0–499.0** w kodzie.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-15:** Plaster **499.0** zamknięty (`/noc 8`) — HITL `shipper_award_mark`.
**2026-09-15:** Plaster **498.0** zamknięty (`/noc 8`) — HITL `shipper_bind_mark`.
**2026-09-15:** Plaster **497.0** zamknięty (`/noc 8`) — HITL `sales_bind_mark`.
**2026-09-15:** Plan **500.0** AI3.0 leftover PATCH quote/rfq — delta OK; kod w kolejnej turze przed 08:00 tylko jeśli starczy wall-clock.
