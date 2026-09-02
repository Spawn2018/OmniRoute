# Bieżący focus

**Faza:** Wave FE leftover (po Fali 11) — tabela leftover pusta  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **57.0** U-print arkusz `@media print` na ofercie / FV / dokumencie zlecenia (zarchiwizowany)  
**Etap:** Idle  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** brak pozycji w kolejce. F9.1 M-58–M-60 bez żywej nazwy — nie zgaduj. Parked: M-02, Auth0, portale.  
M-02 **parked**. Auth0 **odroczone**. Portale **parked**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak — kolejka leftover pusta. Nie otwieraj [print-sheet.md](../spec/print-sheet.md) jako następnego Q.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 57.0 zamknięty. Kolejka leftover pusta do godziny stopu `/noc`.
