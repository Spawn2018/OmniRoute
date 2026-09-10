# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **267.0** leftover HITL `lane_km`  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-11T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md).  
**Następny:** leftover F9 Optima fixture (delta 268.0 accepted `/noc`, wolno `/plaster`) → T8 → S53 Auth0 → portale/diada → CT7/CI9/reszta pinu 2026-09-08c. Leftover HITL/SQL = praca. Park = live HTTP bez testu albo sekretu, nie skip pola. Live M-02 konsument / Auth0 / portale tylko gdy ten ID jest bieżącym Q. P6c auto-award zakaz. Nic z pinu nie wypada. Nie zgaduj 71–268.  
M-02 **fundament 79.0** (konsument = krok osi T5, nie skip nocy). Auth0 = S53 gdy CURRENT dojdzie. Portale **po S53**. S21 live HTTP = park live. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c `driver2` = 212.0; leftover T2 `route_label` = 214.0; leftover T2c km = 256.0/257.0; leftover `party` = 258.0; leftover `/fleet` = 259.0). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [268.0-erp-connector.md](../deltas/open/268.0-erp-connector.md) · [erp-connector.md](../spec/erp-connector.md). Komenda `/plaster`. Oś: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. Karty [erp-fk-adapter.md](../analysis/erp-fk-adapter.md) (tylko Optima). Nie G2.22 P/lista w tym Q (oś: F9 przed G2.22). Nie RAG na stawkach / umowach CI. Nie pgvector. Nie T8 live API. Nie drugi czat. Nie N8. Nie live VIES. Nie auto-award. Nie scrape. Nie Citizen API. Nie silnik ≥500k. Nie kalkulator kg. Nie live PUESC/KSeF. Nie 409 na shipment. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo HTTP. Nie myto. Nie countdown D&D. Nie live GPS. Nie sekrety adaptera. Nie scoring osoby. Nie silnik EBITDA. Nie fizyka twinów. ExtractionService nie importuje tenders/rates. LLM nie sumuje.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. **267.0** zamknięty (`/noc`) — HITL `lane_km`. Delta **268.0** accepted (`/noc`) — HITL `erp_connector` kind `optima`, fixture, zero sekretów. Wolno `/plaster`. Nie live SOAP. Nie XL. Nie G2.22. `/noc` nie pomija osi. LLM nie liczy.
