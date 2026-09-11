# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **290.0** leftover CT4 matching lane/mode na shipment  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **291.0** leftover CT1 HITL promote ASN → shipment.  
Park: U1 masowy · qty float · wspólny SELECT · SQL FV vs charge · workflow CAPA · live SOAP · CT2 · CT5/CT8 live. Nie CI1 extract. Nie zgaduj 71–290.

**Spec (jedyna na sesję):** [docs/spec/asn-promote-shipment.md](../spec/asn-promote-shipment.md) · delta [docs/deltas/open/291.0-asn-promote-shipment.md](../deltas/open/291.0-asn-promote-shipment.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** HITL zostaje. LLM nie liczy. `charge` = marża. Auto przy POST asn nie jest done. Nota 4,4–5 = karta i diff.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` w PATH. PG 16: `tools\pg16`.

**2026-09-08c:** Plan **291.0** promote ASN→shipment zaakceptowany nocą — kod.
