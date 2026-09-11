# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **290.0** leftover CT4 matching lane/mode na shipment  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover Fala CT / pin — wspólny SELECT / auto shipment / CT2 albo następny wąski HITL z PLAN.  
Park: wspólny SELECT · SQL FV vs charge · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live. Nie CI1 extract. Nie zgaduj 71–290.

**Spec (jedyna na sesję):** brak — następne Q z osi leftoverów. Komenda `/plan-modul`.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** **290.0** zamknięty (`/noc`) — label match na shipment. Następne Q = plan leftover CT / pin.
