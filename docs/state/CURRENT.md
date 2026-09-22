# Bieżący focus

**Faza:** Oś pinu — plan **619.0** (U3c pule air)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **618.0** T7d `charge_sell_in_pln` (lokalnie; CI po push)

**Etap:** Plan **619.0**. Komenda `/plan-modul`.

**Noc:** `/noc 7` do **2026-09-22T07:00:00+02:00**

**Miejsce pracy:** produkt = to repo + GitHub.

**Następny:** **619.0** U3c leftover pule IATA/air. Daty bazowe zlecenia / matching T5 / FK kontekstu / T8 live = park `/noc`. **588.0** SH-R16-4 UXCL = park `/noc`.

**Park / czeka w PLAN:** daty bazowe · fx×FV compose · matching T5 · FK kontekstu · T8 live · HW · SH-R16-4 UXCL · AI3 · G0-SH · N3 · …

**Spec (jedyna na sesję produktu):** brak — najpierw delta **619.0** (`/plan-modul`).

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL. LLM nie liczy. `charge` = marża.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-22:** Plaster **618.0** T7d `charge_sell_in_pln` zamknięty lokalnie (CI po push). `/noc 7`.
**2026-09-22:** Plan **618.0** T7d przeliczenie kursu w SQL (`/noc 7`). 617.0 gate success.
**2026-09-22:** Plaster **617.0** T7c `fx_rate_day` zamknięty (gate success). `/noc 7`.
**2026-09-22:** Plaster **617.0** T7c `fx_rate_day` zamknięty lokalnie (CI po push). `/noc 7`.
**2026-09-21:** Plan **617.0** T7c dzień roboczy U4 przy offsecie kursu (`/noc 7`). 616.0 gate success.
**2026-09-21:** Plaster **616.0** T5 `task` HITL zamknięty (gate success). `/noc 7`.
**2026-09-21:** Plaster **616.0** T5 `task` HITL zamknięty lokalnie (CI po push). `/noc 7`.
**2026-09-21:** Plan **616.0** T5 `task` HITL (`/noc 7`). 615.0 gate success.
**2026-09-21:** Plaster **615.0** T7b `fx_rate_*` na `charge` zamknięty (gate success). `/noc 7`.
**2026-09-21:** Plan **615.0** T7b `fx_rate_*` na `charge` (`/noc 7`). 614.0 gate success.
**2026-09-21:** Plaster **614.0** T4 `shipment_tree_margin` zamknięty (gate success). `/noc 7`.
**2026-09-21:** Plan **614.0** T4 widok `shipment_tree_margin` (`/noc 7`). 613.0 gate success.
**2026-09-21:** Plaster **613.0** T4 `charge.shipment_id` zamknięty lokalnie (CI po push). `/noc 7`.
**2026-09-21:** Plan **613.0** T4 `charge.shipment_id` (`/noc 7`). Rollup SQL parked. 612.0 gate success.
