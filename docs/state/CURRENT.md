# Bieżący focus

**Faza:** Fala S — leftover S7 UN na RFQ (po 121.0)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **121.0** leftover S11 `changed` na `operator_decision` (M-71)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** `/plan-modul` leftover S7 **UN z M-52** na RFQ. Nie LLM. Nie F9.1.  
M-02 **fundament 79.0**. Auth0 **odroczone** (S53). Portale **parked** (S55). S21 live HTTP **parked**. S50 flota **named park**. S54 status klienta **named park**. S59 OTel/QA/rollout **named park**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** [docs/spec/dangerous-good.md](../spec/dangerous-good.md) po akceptacji delty. Nie otwieraj [operator-decision.md](../spec/operator-decision.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Cel jakości + § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations. Nota 4,4–5 = karta i diff, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-04:** 121.0 zamknięty (`/noc`). Następny named leftover: UN na RFQ. Nie zgaduj 71–212.
