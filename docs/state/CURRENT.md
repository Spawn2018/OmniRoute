# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **279.0** leftover HITL `routing_guide`  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover Fala CT / pin — CT3 OTIF katalog albo CT1 auto shipment compose (parked z powodem) / egzekucja 409 / CT2 gdy CI5. CT5 EDI live = park. CT8 AIS = park live. Nie CI1 extract. Nie live p44. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu. Nie zgaduj 71–279.  
CT1 **276–278**. CT4 HITL `routing_guide` **279.0** (nie 409). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak — następne Q z osi leftoverów. Komenda `/plan-modul`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). 279.0 = katalog przewodnika, nie 409. Auto shipment / CT2 parked z powodem w delcie 279.0. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Auto shipment nie jest done — parked. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** **279.0** zamknięty (`/noc`) — HITL `routing_guide`. Następne Q = plan leftover CT / pin. `/noc` nie pomija osi.
