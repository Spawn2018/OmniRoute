# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **171.0** G2.2 `tender_lane`  
**Etap:** Kod  
**Noc:** `/noc 7` do 2026-09-09T07:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Billing GitHub zablokowany — ta sesja nie czeka na zielone CI.  
**Następny:** **172.0** G2.3 `tender_round` → G2.4–G2.23 → F → C → V → W → S53 → X → WA1 → Plat → Demo-1 → CT → CI9–CI8 → G → EXP → Mob → K0. D8 parked. D9 leftover D9b–f. P1 leftover P1b–d. P2 leftover P2c. P3 leftover P3b–d. P4 leftover P4b–c. P5 leftover P5b–c. P6 leftover P6c. G2 leftover G2.4–G2.18. Named parks parked — `/noc` pomija aż CURRENT wskaże S53. Nic z pinu 2026-09-08c nie wypada. Nie zgaduj 71–212.  
M-02 **fundament 79.0** (konsument leftover — parked aż T5/X4). Auth0 **odroczone** (S53 w osi po W). Portale **po S53**. S21 live HTTP **parked**. S50 = T2 (`resource` 151.0, `trip` 152.0; leftover T2c). S54 / S59 / AIS leftover parked. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/deltas/open/172.0-tender-round.md](../deltas/open/172.0-tender-round.md). Oś: karty `karty-pol-fala-*.md`. Nie otwieraj spec C8.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. Delta **172.0** zaakceptowana (`/noc`). Wolno `/plaster`. Nie auto-award. Nie T-SQL.
