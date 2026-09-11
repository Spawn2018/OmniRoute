# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **280.0** leftover HITL `otif_mark`  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover Fala CT / pin — CT6 HITL konektor SAP/Oracle (jak F9) albo CT12 CAPA katalog albo egzekucja 409 z `routing_guide`.  
Park: CT1 auto shipment · CT2 CI5 · CT5 EDI live · CT8 AIS live · OTIF%. Nie CI1 extract. Nie live p44. Leftover HITL/SQL = praca. Nie zgaduj 71–280.

**Spec (jedna na sesję):** brak — następne Q z osi leftoverów. Komenda `/plan-modul`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). 280.0 = katalog zakresu OTIF, nie %. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. OTIF% nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** **280.0** zamknięty (`/noc`) — HITL `otif_mark`. Następne Q = plan leftover CT / pin.
