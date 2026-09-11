# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **285.0** leftover HITL `routing_guide_enforcement`  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **286.0** leftover CT4 żywy HTTP 409 na ASN poza guide.  
Park: 409 na shipment · wspólny SELECT · SQL FV vs charge · workflow CAPA · live SOAP · auto shipment · CT2 · CT5/CT8 live. Nie CI1 extract. Nie zgaduj 71–286.

**Spec (jedna na sesję):** [docs/spec/asn-routing-guide-409.md](../spec/asn-routing-guide-409.md) · delta [docs/deltas/open/286.0-asn-routing-guide-409.md](../deltas/open/286.0-asn-routing-guide-409.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. 409 na shipment nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** Plan **286.0** ASN 409 zaakceptowany nocą — kod.
