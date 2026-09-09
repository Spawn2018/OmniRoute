# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **195.0** V2 `weather_observation`  
**Etap:** Plan  
**Noc:** `/noc 17` do 2026-09-09T17:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Billing GitHub zablokowany — ta sesja nie czeka na zielone CI.  
**Następny:** **196.0** V3 D&D/rollover HITL → leftover V2b myto→`charge` parked → leftover C3 live VIES/GUS → leftover C4 eCMR → leftover C9 Trans.eu → leftover C2 AIS/PUESC → leftover C6 BDO → leftover F2b Decimal/rezerwy → leftover F3 noty/period lock → leftover F4 CAMT → leftover G2.20–G2.22 circle_sim/km/P → leftover G2.15–G2.18 kg/CBAM → leftover F1 live FA(3) → leftover C1 filing XML → leftover C8 409/`relation_document_requirement` → C → V → W → S53 → X → WA1 → Plat → Demo-1 → CT → CI9–CI8 → G → EXP → Mob → K0. D8 parked. D9 leftover D9b–f. P1 leftover P1b–d. P2 leftover P2c. P3 leftover P3b–d. P4 leftover P4b–c. P5 leftover P5b–c. P6 leftover P6c. G2 leftover G2.15–G2.18 + G2.20–G2.22 + G2.23 Citizen API. Named parks parked — `/noc` pomija aż CURRENT wskaże S53. Nic z pinu 2026-09-08c nie wypada. Nie zgaduj 71–212.  
M-02 **fundament 79.0** (konsument leftover — parked aż T5/X4). Auth0 **odroczone** (S53 w osi po W). Portale **po S53**. S21 live HTTP **parked**. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c). S54 / S59 / AIS leftover parked. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak. Wolno `/plan-modul`. Oś: karty `karty-pol-fala-*.md`. Nie otwieraj spec C3 live VIES. Nie auto-award. Nie scrape. Nie Citizen API. Nie circle_sim. Nie kalkulator kg. Nie live PUESC/KSeF. Nie 409 na shipment. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo HTTP. Nie myto. Nie scoring osoby. ExtractionService nie importuje tenders/rates.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. Delta **195.0** zamknięta (`/noc`). Wolno `/plan-modul` na **196.0**. Nie auto-award. Nie T-SQL. Nie scrape. Nie live HTTP. Nie kalkulator kg. Nie circle_sim. Nie 409 na shipment. Nie kwota na skonto. Nie CAMT. Nie silnik CRPS. Nie Open-Meteo. Nie myto. Nie scoring osoby. LLM nie liczy.
