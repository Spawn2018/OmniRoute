# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **285.0** leftover HITL `routing_guide_enforcement`  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover żywy HTTP 409 na shipment/ASN poza guide (pin 2026-09-08c).  
    Park: wspólny SELECT · CT9 (już C5) · SQL FV vs charge · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live. Nie CI1 extract. Nie zgaduj 71–285.

**Spec (jedna na sesję):** brak otwartej delty — plan leftoveru żywy 409 albo następny pin z PLAN § Kolejka.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Żywy 409 na zleceniu nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** Plan **285.0** CT4 enforcement zaakceptowany nocą — zamknięty.
