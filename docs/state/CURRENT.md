# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **283.0** leftover HITL `freight_audit_mark`  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **284.0** leftover CT11 HITL `collaboration_mark` (rola shipper|carrier|consignee).  
Park: wspólny SELECT · tuple OpenFGA 3 strony · egzekucja 409 · SQL FV vs charge · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live · CT9. Nie CI1 extract. Nie zgaduj 71–284.

**Spec (jedna na sesję):** [docs/spec/collaboration-mark.md](../spec/collaboration-mark.md) · delta [docs/deltas/open/284.0-collaboration-mark.md](../deltas/open/284.0-collaboration-mark.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Wspólny SELECT nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** **283.0** zamknięty (`/noc`). Plan **284.0** CT11 zaakceptowany nocą — kod.
