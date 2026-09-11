# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **289.0** leftover CT4 matching lane/mode na ASN  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **290.0** leftover CT4 matching lane/mode na shipment (`plant_label`/`carrier_label` + ten sam gate co ASN).  
Park: wspólny SELECT · SQL FV vs charge · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live. Nie CI1 extract. Nie zgaduj 71–289.

**Spec (jedyna na sesję):** [docs/spec/shipment-lane-mode-match.md](../spec/shipment-lane-mode-match.md) · delta [docs/deltas/open/290.0-shipment-lane-mode-match.md](../deltas/open/290.0-shipment-lane-mode-match.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Matching na shipment = ten plaster. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** Plan **290.0** (`/noc`) — etykiety na shipment pod match 288.0.
