# Bieżący focus

**Faza:** Fala 6 — finanse  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **35.0** M-42 `bank_payment` tablica `/payments` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 36.0 M-43 `money_cost` tablica `/money-cost`. Nie zgaduj schematu. Nie nowa tabela.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 6.

**Spec (jedna na sesję):** [money-cost.md](../spec/money-cost.md) — delta [36.0-money-cost.md](../deltas/open/36.0-money-cost.md).

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** nie zgaduj tabeli kosztu pieniądza. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** delta 36.0 zaakceptowana `/noc`. Wolno `/plaster`.
