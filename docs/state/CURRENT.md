# Bieżący focus

**Faza:** Fala S — pogłębienie wydmuszek (po Fali E)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **116.0** S56 copilot na wieży (M-57)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** `/plaster` **117.0** — S57 narracja po SQL (M-15). LLM nie liczy. Nie F9.1.  
M-02 **fundament 79.0**. Auth0 **odroczone** (S53). Portale **parked** (S55). S21 live HTTP **parked**. S50 flota **named park**. S54 status klienta **named park**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/deltas/open/117.0-finance-narrative.md](../deltas/open/117.0-finance-narrative.md). Nie otwieraj [ai-copilot.md](../spec/ai-copilot.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Cel jakości + § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations. Nota 4,4–5 = karta i diff, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-04:** plan 117.0 zaakceptowany (`/noc`). Wolno `/plaster`. Nie F9.1.
