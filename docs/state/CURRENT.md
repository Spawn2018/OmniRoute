# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **287.0** leftover CT4 409 na shipment poza guide  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **288.0** leftover CT4 HITL `routing_guide_match` (tryb guide_code_only|lane_label|mode_label).  
Park: silnik matching · wspólny SELECT · SQL FV vs charge · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live. Nie CI1 extract. Nie zgaduj 71–288.

**Spec (jedna na sesję):** [docs/spec/routing-guide-match.md](../spec/routing-guide-match.md) · delta [docs/deltas/open/288.0-routing-guide-match.md](../deltas/open/288.0-routing-guide-match.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Silnik matching nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** Plan **288.0** match kind zaakceptowany nocą — kod.
