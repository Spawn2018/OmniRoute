# Bieżący focus

**Faza:** Fala S — pogłębienie wydmuszek (po Fali E)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **66.0** S3 treść `inbound_message` → extract HITL  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`. Etap Plan → `/plan-modul`, nie `/plaster`.  
**Następny:** S4 `/plan-modul` — obiekt RFQ powiązany z wiadomością. Nie ślad wycen. Nie IMAP. Nie F9.1.  
M-02 **parked** (odblokowanie S16). Auth0 **odroczone** (S53). Portale **parked** (S55). Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak delty S4. Nie otwieraj [print-sheet.md](../spec/print-sheet.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Cel jakości + § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations. Nota 4,4–5 = karta i diff, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 66.0 zamknięty (`/noc`). Następny: `/plan-modul` S4. Nie F9.1.
