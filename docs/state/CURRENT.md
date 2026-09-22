# Bieżący focus

**Faza:** Oś pinu — plaster **624.0** (D4b rodzaj dokumentu rod)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **623.0** D7d `pallet_kind=epal` (gate success)

**Etap:** Plaster **624.0**. Delta zaakceptowana. Wolno `/plaster`.

**Noc:** `/noc 17` do **2026-09-22T17:00:00+02:00**

**Miejsce pracy:** produkt = to repo + GitHub.

**Następny:** **624.0** D4b POD/ROD na dokumencie zlecenia (HITL, nie skan). Daty bazowe zlecenia / matching T5 / FK kontekstu / T8 live / D6b konsolidacja / D7b giełda = park `/noc`. **588.0** SH-R16-4 UXCL = park `/noc`.

**Park / czeka w PLAN:** daty bazowe · fx×FV compose · matching T5 · FK kontekstu · T8 live · D6b · HW · SH-R16-4 UXCL · AI3 · G0-SH · N3 · …

**Spec (jedyna na sesję produktu):** [624.0-shipment-document-rod.md](../deltas/open/624.0-shipment-document-rod.md).

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL. LLM nie liczy. `charge` = marża.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-22:** Plan **624.0** D4b `document_kind=rod` (`/noc 17`). 623.0 gate success.
**2026-09-22:** Plaster **623.0** D7d `epal` na saldzie palet zamknięty lokalnie (CI po push). `/noc 17`.
**2026-09-22:** Plan **623.0** D7d `pallet_kind=epal` na saldzie palet (`/noc 17`). 622.0 gate success.
**2026-09-22:** Plaster **622.0** U3 cyfra kontrolna IATA na MAWB zamknięty lokalnie (CI po push). `/noc 17`.
**2026-09-22:** Plan **622.0** U3 cyfra kontrolna IATA na wklejonym MAWB (`/noc 17`). 621.0 gate po push.
**2026-09-22:** Plaster **621.0** D6c pule HBL/MBL zamknięty (`/noc 7`).
**2026-09-22:** Plan **621.0** D6c pule HBL/MBL z M-03 (`/noc 7`). 620.0 gate success.
**2026-09-22:** Plaster **620.0** U3 e-rates air zamknięty (gate success). `/noc 7`.
**2026-09-22:** Plan **620.0** U3 e-rates air na `channel_quote` (`/noc 7`). 619.0 gate success.
**2026-09-22:** Plaster **619.0** U3c pule HAWB/MAWB zamknięty (gate success). `/noc 7`.
**2026-09-22:** Plan **619.0** U3c pule HAWB/MAWB z M-03 (`/noc 7`). 618.0 gate success.
**2026-09-22:** Plaster **618.0** T7d `charge_sell_in_pln` zamknięty (gate success). `/noc 7`.
**2026-09-22:** Plan **618.0** T7d przeliczenie kursu w SQL (`/noc 7`). 617.0 gate success.
**2026-09-21:** Plan **617.0** T7c dzień roboczy U4 przy offsecie kursu (`/noc 7`). 616.0 gate success.
**2026-09-21:** Plaster **616.0** T5 `task` HITL zamknięty (gate success). `/noc 7`.
**2026-09-21:** Plan **616.0** T5 `task` HITL (`/noc 7`). 615.0 gate success.
**2026-09-21:** Plaster **615.0** T7b `fx_rate_*` na `charge` zamknięty (gate success). `/noc 7`.
**2026-09-21:** Plan **615.0** T7b `fx_rate_*` na `charge` (`/noc 7`). 614.0 gate success.
**2026-09-21:** Plaster **614.0** T4 `shipment_tree_margin` zamknięty (gate success). `/noc 7`.
**2026-09-21:** Plan **614.0** T4 widok `shipment_tree_margin` (`/noc 7`). 613.0 gate success.
**2026-09-21:** Plaster **613.0** T4 `charge.shipment_id` zamknięty lokalnie (CI po push). `/noc 7`.
**2026-09-21:** Plan **613.0** T4 `charge.shipment_id` (`/noc 7`). Rollup SQL parked. 612.0 gate success.
