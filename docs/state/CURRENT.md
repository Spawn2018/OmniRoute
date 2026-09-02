# Bieżący focus

**Faza:** Fala E — jakość 4,4–5 (po Fali 11)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **61.0** Q-E2 testy przez Alembic + pomiar wyceny  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`. Etap Plan → `/plan-modul`, nie `/plaster`.  
**Następny:** 62.0 Q-E3 `/plaster` — how-to jobów zapisu + C4 w ARCHITECTURE. Nie 70 stubów. Nie F9.1. Nie S1. Parked: M-02, Auth0, portale (odblokowanie w Fali S).  
M-02 **parked**. Auth0 **odroczone**. Portale **parked**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [62.0-operator-howto-c4.md](../deltas/open/62.0-operator-howto-c4.md). Nie otwieraj [print-sheet.md](../spec/print-sheet.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Cel jakości + § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations. Nota 4,4–5 = karta i diff, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Delta 62.0 zaakceptowana (`/noc`). Następny: `/plaster` 62.0. Po Q-E4: Fala S, start S1 (M-32 tabela wiadomości) — nie F9.1.
