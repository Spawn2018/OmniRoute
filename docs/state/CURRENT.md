# Bieżący focus

**Faza:** Fala 5 — zlecenie  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **30.0** M-37 `operational_exception` tablica `/exceptions` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** M-38 Dokumenty zlecenia (`/plan-modul`). Nie zgaduj schematu. Nie nowa tabela.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 5.

**Spec (jedna na sesję):** brak do `/plan-modul` — nie otwieraj [operational-exception.md](../spec/operational-exception.md) jako kolejki M-38.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** nie zgaduj tabeli dokumentów zlecenia. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 30.0 na kolejce zamknięcia. Następny: `/plan-modul` M-38 (nie nowa rozmowa w `/noc`).
