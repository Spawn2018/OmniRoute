# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **260.0** leftover N1 `consignment`  
**Etap:** Plan  
**Noc:** `/noc 17` do 2026-09-10T17:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **261.0** leftover T6 mapa → SQL `charge` → lookup/KSeF TE → outbox T5 → `plan_snapshot`/kółka → F9 Optima fixture → T8 → S53 Auth0 → portale/diada → CT7/CI9/reszta pinu 2026-09-08c. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu, nie skip pola. Live M-02 konsument / Auth0 / portale tylko gdy ten ID jest bieżącym Q. P6c auto-award zakaz. Nic z pinu nie wypada. Nie zgaduj 71–261.  
M-02 **fundament 79.0** (konsument = krok osi T5, nie skip nocy). Auth0 = S53 gdy CURRENT dojdzie. Portale **po S53**. S21 live HTTP = park live. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c `driver2` = 212.0; leftover T2 `route_label` = 214.0; leftover T2c km = 256.0/257.0; leftover `party` = 258.0; leftover `/fleet` = 259.0). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak otwartej delty. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. Karty `karty-pol-fala-*.md`. Następna komenda: `/plan-modul` **261.0** (węższe z leftover: T6 mapa). Nie RAG na stawkach / umowach CI. Nie pgvector. Nie T8 live API. Nie drugi czat. Nie N8. Nie live VIES. Nie auto-award. Nie scrape. Nie Citizen API. Nie circle_sim. Nie kalkulator kg. Nie live PUESC/KSeF. Nie 409 na shipment. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo HTTP. Nie myto. Nie countdown D&D. Nie live GPS. Nie sekrety adaptera. Nie scoring osoby. Nie silnik EBITDA. Nie fizyka twinów. ExtractionService nie importuje tenders/rates. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. Delta **260.0** zamknięta. Wolno `/plan-modul` 261.0. W **następnym** plasterze: T6 tablica planowania + mapa lazy (paczka poza 250 kB), nie GPS live, nie PIN, nie SQL na `charge`, nie T5, nie auto-award, nie T-SQL. Kolejne Q z osi jadą po zamknięciu 261.0 — `/noc` ich nie pomija. LLM nie liczy.
