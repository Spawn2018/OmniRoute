# Bieżący focus

**Faza:** Oś pinu **528.0+** (N9)

**Repo:** https://github.com/Spawn2018/OmniRoute

**Ostatni plaster:** **527.0** N6 — HITL `margin_floor` Decimal

**Etap:** Plan **528.0** zaakceptowana — wolno `/plaster`

**Noc:** **busy** do 07:00+02. Po pushu delty: plaster **528.0**. Rytuały **SH-R16-12…15** tylko przy idle/P-Y.

**Miejsce pracy:** produkt = to repo + GitHub. Kanon SH: [rejestr-wdrozenia-16-ix.md](../ops/rejestr-wdrozenia-16-ix.md) §5. Playbooki: [fabryka-playbooki-sh.md](../ops/fabryka-playbooki-sh.md).

**Następny:** **528.0** N9 — HITL `shipment_clone_mark` (intencja klonu; nie drugi SoR)

**Park / czeka w PLAN:** SH-R16-12 pulse · SH-R16-13 Dependabot 1/tyg · SH-R16-14 fire skill · SH-R16-15 PARK-RADAR · UXCL-L1 · AI3-payload · Plat-HD-flow · G0 · leftover N6 409/S11 · leftover N9 copy/U1 · … Nie AI0.

**Spec (jedyna na sesję produktu):** [docs/deltas/open/528.0-shipment-clone-mark.md](../deltas/open/528.0-shipment-clone-mark.md)

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — § Fala SH-R16 (0…15). Wizja: [VISION.md](../VISION.md).

**Uczciwość:** HITL. LLM nie liczy. `charge` = marża. Szablony SH **29/29**. False DONE z audytu naprawione.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-16:** Plan **528.0** N9 `shipment_clone_mark` (delta).
**2026-09-16:** Plaster **527.0** `margin_floor` HITL; leftover 409/S11; CI gate success.
**2026-09-16:** Audyt braków → SH-R16-8…11 DONE; 12…15 w kolejce rytuałów.
**2026-09-16:** `/noc 7` od ~03:57.
