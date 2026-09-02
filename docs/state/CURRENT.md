# Bieżący focus

**Faza:** Fala 5 — zlecenie  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **29.0** M-36 `tracking` tablica `/tracking` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** `/plaster` 30.0 M-37 `operational_exception` tablica `/exceptions`. Nie nowa tabela. Nie zgaduj schematu zdarzeń.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 5.

**Spec (jedna na sesję):** [docs/spec/operational-exception.md](../spec/operational-exception.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** nie zgaduj tabeli wyjątków. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 29.0 zamknięty. Plan 30.0 M-37 na `/exceptions`. Następny: `/plaster` (nie nowa rozmowa w `/noc`).
