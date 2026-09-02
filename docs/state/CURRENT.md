# Bieżący focus

**Faza:** Fala E — jakość 4,4–5 (po Fali 11)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **59.0** kanon jakości 4,4–5 w PLAN + kolejka Q-E  
**Etap:** Refaktor  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`. Etap Refaktor → `/refaktor`, nie `/plaster`.  
**Następny:** Q-E1 `/refaktor` — katalogi Grupa A do 4,4 (`catalog-parts`). Nie F9.1. Parked: M-02, Auth0, portale.  
M-02 **parked**. Auth0 **odroczone**. Portale **parked**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Cel jakości i § Kolejka Q-E1. Nie otwieraj [print-sheet.md](../spec/print-sheet.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Cel jakości + § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations. Nota 4,4–5 = karta i diff, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 59.0 zamknięty. Następny: `/refaktor` Q-E1.
