# Bieżący focus

**Faza:** Fala 7 — modały  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **40.0** M-47 `bookkeeping` tablica `/bookkeeping` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** M-48 Transport drogowy (`/plan-modul`). Nie zgaduj schematu. Nie nowa tabela.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 7.

**Spec (jedna na sesję):** brak do `/plan-modul` — nie otwieraj [bookkeeping.md](../spec/bookkeeping.md) jako kolejki M-48.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** nie zgaduj tabeli drogówki. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 40.0 na kolejce zamknięcia. Następny: `/plan-modul` M-48 (nie nowa rozmowa w `/noc`).
