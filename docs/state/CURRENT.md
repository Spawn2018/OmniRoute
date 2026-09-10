# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **274.0** leftover HITL `tenant_contract_kek` znacznik owijki  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover CT7 parked live / reszta pinu 2026-09-08c. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu, nie skip pola. Live M-02 konsument / Auth0 I1/I2 / portale / giełda live tylko gdy ten ID jest bieżącym Q. P6c auto-award zakaz. Nic z pinu nie wypada. Nie zgaduj 71–275.  
M-02 **fundament 79.0** (konsument = krok osi T5, nie skip nocy). S53 HITL `idp_connector` **270.0**. S55 HITL `exchange_connector` **271.0**. CI9 HITL `customer_contract` nagłówek **272.0**. CI9 opaque BYTEA **273.0** (present/absent, nie szyfr). CI9 znacznik owijki **274.0** (nie klucz, nie szyfr). S21 live HTTP = park live. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c `driver2` = 212.0; leftover T2 `route_label` = 214.0; leftover T2c km = 256.0/257.0; leftover `party` = 258.0; leftover `/fleet` = 259.0). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak — następne Q to leftover CT7 parked live / reszta pinu. Komenda `/plan-modul`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. 272.0 = nagłówek; 273.0 = opaque blob present/absent, nie szyfr. 274.0 = znacznik, nie klucz. Nie KMS. Nie unwrap. Nie `wrapped_dek`. Nie Fernet/AES. Nie materiał klucza. Nie CT7 live. Nie CI1 extract. Nie `sla_clause`. Nie super-admin plaintext (nie ma decode). Nie G2.22 P/lista. Nie RAG na stawkach / umowach CI. Nie pgvector. Nie T8 live API. Nie drugi czat. Nie N8. Nie live VIES. Nie auto-award. Nie scrape. Nie Citizen API. Nie silnik ≥500k. Nie kalkulator kg. Nie live PUESC/KSeF. Nie 409 na shipment. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo HTTP. Nie myto. Nie countdown D&D. Nie live GPS. Nie sekrety adaptera. Nie scoring osoby. Nie silnik EBITDA. Nie fizyka twinów. ExtractionService nie importuje tenders/rates i **nie** widzi umów CI ani znacznika KEK. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. **273.0 = present/absent, nie szyfr. 274.0 = znacznik, nie klucz.** CT7 live nie istnieje. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. **274.0** zamknięty (`/noc`) — HITL znacznik owijki, nie klucz. 273.0 nadal present/absent, nie szyfr. Następne Q = plan leftover CT7 parked live / reszta pinu, nie CI1. `/noc` nie pomija osi. LLM nie liczy.
