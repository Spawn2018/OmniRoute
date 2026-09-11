# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **278.0** leftover HITL `asn`  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **279.0** leftover CT4 HITL `routing_guide` (katalog; nie 409 egzekucja). CT1 auto shipment = parked (quotation_id + zakaz FK shipment w BC PO). CT2 = parked (CI5 brak). CT8 AIS = park live. Nie CI1 extract. Nie live p44. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu, nie skip pola. Live M-02 konsument / Auth0 I1/I2 / portale / giełda live / p44 live tylko gdy ten ID jest bieżącym Q. P6c auto-award zakaz. Nic z pinu nie wypada. Nie zgaduj 71–279.  
CT1 HITL `purchase_order` **276.0** · `po_line` **277.0** · `asn` **278.0**. CT4 HITL `routing_guide` **279.0**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/deltas/open/279.0-routing-guide.md](../deltas/open/279.0-routing-guide.md) — HITL katalog przewodnika routingu. Komenda `/plaster`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. 279.0 = katalog, nie 409. Nie auto shipment. Nie CI5. Nie KMS. Nie live EDI. Nie AIS. ExtractionService nie widzi umów CI. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. CT1 auto shipment nie jest „done” — parked z powodem w delcie 279.0. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. **278.0** zamknięty. Delta **279.0** zaakceptowana (`/noc`) — HITL `routing_guide`, nie 409. Auto shipment / CT2 parked z powodem. `/noc` nie pomija osi. LLM nie liczy.
