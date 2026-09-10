# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **271.0** leftover HITL `exchange_connector` Trans.eu fixture  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** kod **272.0** leftover HITL `customer_contract` nagłówek (CI9). Po zamknięciu: leftover CI9 ciphertext/KEK (park KMS/unwrap) albo CT7 parked live / reszta pinu 2026-09-08c. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu, nie skip pola. Live M-02 konsument / Auth0 I1/I2 / portale / giełda live tylko gdy ten ID jest bieżącym Q. P6c auto-award zakaz. Nic z pinu nie wypada. Nie zgaduj 71–272.  
M-02 **fundament 79.0** (konsument = krok osi T5, nie skip nocy). S53 HITL `idp_connector` **270.0**. S55 HITL `exchange_connector` **271.0**. CI9 HITL `customer_contract` header = ten Q. S21 live HTTP = park live. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c `driver2` = 212.0; leftover T2 `route_label` = 214.0; leftover T2c km = 256.0/257.0; leftover `party` = 258.0; leftover `/fleet` = 259.0). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/deltas/open/272.0-customer-contract.md](../deltas/open/272.0-customer-contract.md) — leftover CI9 HITL nagłówek umowy (kod + etykiety załadowca/odbiorca + `source_ref`). Delta zaakceptowana (`/noc`). Wolno `/plaster`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. Nie ciphertext. Nie KEK/KMS. Nie CT7 live. Nie CI1 extract. Nie `sla_clause`. Nie super-admin plaintext. Nie G2.22 P/lista. Nie RAG na stawkach / umowach CI. Nie pgvector. Nie T8 live API. Nie drugi czat. Nie N8. Nie live VIES. Nie auto-award. Nie scrape. Nie Citizen API. Nie silnik ≥500k. Nie kalkulator kg. Nie live PUESC/KSeF. Nie 409 na shipment. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo HTTP. Nie myto. Nie countdown D&D. Nie live GPS. Nie sekrety adaptera. Nie scoring osoby. Nie silnik EBITDA. Nie fizyka twinów. ExtractionService nie importuje tenders/rates i **nie** widzi umów CI. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Ten Q = nagłówek, nie szyfr. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. **271.0** zamknięty (`/noc`) — HITL `exchange_connector` token `trans_eu`, zero live giełdy, zero SPA. Plan **272.0** zaakceptowany (`/noc`) — HITL `customer_contract` nagłówek, zero ciphertext, zero CT7 live. `/noc` nie pomija osi. LLM nie liczy.
