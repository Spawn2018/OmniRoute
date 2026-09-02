# Bieżący focus

**Faza:** Fala 2 — M-15 Wirtualny Dyrektor Finansowy  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **14.0** M-14 `credit_review` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 15.0 M-15 `finance_board` (`/plaster`). LLM nie liczy. Nie nowa tabela.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** [docs/spec/finance-board.md](../spec/finance-board.md) — nie otwieraj `credit-review.md` jako kolejki 15.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 15.0 tablica odczytu, nie silnik AI. Nie liczyć marży w JS. Nie nadpisywać `charge` ani `credit_limit`. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 15.0 na kolejce. Następny: `/plaster` 15.0 (nie nowa rozmowa w `/noc`).
