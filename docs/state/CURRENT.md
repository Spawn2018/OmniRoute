# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **283.0** leftover HITL `freight_audit_mark`  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover Fala CT / pin — egzekucja 409 z `routing_guide` albo CT9/CT11 gdy węższe HITL.  
Park: SQL FV vs charge · druga marża · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live · OTIF%. Nie CI1 extract. Nie zgaduj 71–283.

**Spec (jedna na sesję):** brak — następne Q z osi leftoverów. Komenda `/plan-modul`.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Audyt FV vs charge nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** **283.0** zamknięty (`/noc`) — HITL `freight_audit_mark`. Następne Q = plan leftover CT / pin.
