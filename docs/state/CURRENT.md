# Bieżący focus

**Faza:** P0 leftover + pełna oś pinu 2026-09-08c (Luki i ulepszenia)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **142.0** O8 `group_by` na `/mail`  
**Etap:** Plan  
**Noc:** `/noc 8` do 2026-09-08T08:00+02. Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Billing GitHub zablokowany — ta sesja nie czeka na zielone CI.  
**Następny:** **N5** cisza agenta / `no_reply_after` → U1+U5 → I1–I4 → U4 → T → U3 → D → P → G2.0–G2.23 → F → C → V → W → S53 → X → WA1 → Plat → Demo-1 → CT → CI9–CI8 → G → EXP → Mob → K0. Named parks parked — `/noc` pomija aż CURRENT wskaże S53. Nic z pinu 2026-09-08c nie wypada. Nie zgaduj 71–212.  
M-02 **fundament 79.0** (konsument leftover — parked aż T5/X4). Auth0 **odroczone** (S53 w osi po W). Portale **po S53**. S21 live HTTP **parked**. S50 = T2. S54 / S59 / AIS leftover parked. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/analysis/karty-pol-fala-n.md](../analysis/karty-pol-fala-n.md) § N5. Oś: karty `karty-pol-fala-*.md`. Nie otwieraj [operator-notice.md](../spec/operator-notice.md) aż delta N5 wskaże ten plik.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka pin **2026-09-08c**.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations i **nie** widzi umów CI. CI9: zero super-admina, zero AI na umowach. Nota 4,4–5 = karta i diff, nie autorecenzja.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test`. PG 16: `tools\pg16`.

**2026-09-08c:** pin całości rozmowy Luki i ulepszenia. O8 **142.0** zamknięty. Następny **N5** — najpierw `/plan-modul`, zero kodu produktu.
