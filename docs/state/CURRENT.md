# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **241.0** leftover T3 `booking_no` na `container`  
**Etap:** Plan  
**Noc:** `/noc 7` do 2026-09-10T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** **242.0** leftover T3 `carrier_party_id` na `container` → `shipment_leg_id` → eventy 2a/2b → `stop_group`/EXP1 → km/`/fleet` → `consignment` → T6 mapa → SQL `charge` → lookup/KSeF TE → outbox T5 → `plan_snapshot`/kółka → F9 Optima fixture → T8 → S53 Auth0 → portale/diada → CT7/CI9/reszta pinu 2026-09-08c. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu, nie skip pola. Live M-02 konsument / Auth0 / portale tylko gdy ten ID jest bieżącym Q. P6c auto-award zakaz. Nic z pinu nie wypada. Nie zgaduj 71–242.  
M-02 **fundament 79.0** (konsument = krok osi T5, nie skip nocy). Auth0 = S53 gdy CURRENT dojdzie. Portale **po S53**. S21 live HTTP = park live. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c `driver2` = 212.0; leftover T2 `route_label` = 214.0; km/`party`/`/fleet` w osi po T3). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** `/plan-modul` **242.0** leftover T3 `carrier_party_id`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. Karty `karty-pol-fala-*.md`. Ten plaster: FK armatora HITL na `container`. Nie RAG na stawkach / umowach CI. Nie pgvector. Nie T8 live API. Nie drugi czat. Nie N8. Nie mapa. Nie live VIES. Nie auto-award. Nie scrape. Nie Citizen API. Nie circle_sim. Nie kalkulator kg. Nie live PUESC/KSeF. Nie 409 na shipment. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo HTTP. Nie myto. Nie countdown D&D. Nie live GPS. Nie sekrety adaptera. Nie scoring osoby. Nie silnik EBITDA. Nie fizyka twinów. ExtractionService nie importuje tenders/rates. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. Delta **241.0** zamknięta (`/noc`). Wolno `/plan-modul` **242.0**. W **tym** planie: `carrier_party_id` HITL, nie PIN, nie live HTTP, nie km, nie `/fleet`, nie nowa tabela `stop_group`, nie SQL na `charge`, nie N1, nie T5, nie mapa, nie auto-award, nie T-SQL. Kolejne Q z osi jadą po zamknięciu 242.0 — `/noc` ich nie pomija. LLM nie liczy.
