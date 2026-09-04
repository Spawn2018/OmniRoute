# Bieżący focus

**Faza:** Fala S — leftover S32 kafelki wieży  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **123.0** leftover S12 filtr kind na tablicy 27.0 (M-34)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** `/plan-modul` leftover S32 kafelki na `/watchtower`. Nie leaflet. Nie F9.1.  
M-02 **fundament 79.0** (konsument leftover — parked). Auth0 **odroczone** (S53). Portale **parked** (S55). S21 live HTTP **parked**. S50 flota **named park**. S54 status klienta **named park**. S59 OTel/QA/rollout **named park**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/deltas/archived/94.0-watchtower.md](../deltas/archived/94.0-watchtower.md) po delcie. Nie otwieraj [operator-notice.md](../spec/operator-notice.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Cel jakości + § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations. Nota 4,4–5 = karta i diff, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-04:** 123.0 na main. Następny leftover S32 kafelki. Nie zgaduj 71–212.
