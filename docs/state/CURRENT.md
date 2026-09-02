# Bieżący focus

**Faza:** Fala 3 — waluty w ofercie  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **15.0** M-15 `finance_board` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 16.0 M-23 `nbp_rate` przy `quotation` (`/plaster`). Czyta katalog 6.0. Nie mnożenie kwoty.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 3.

**Spec (jedna na sesję):** [docs/spec/quotation-nbp.md](../spec/quotation-nbp.md) — nie otwieraj `finance-board.md` ani `nbp-rate.md` jako kolejki 16.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 16.0 odczyt kursu przy wycenie, nie drugi katalog, nie przeliczenie `amount`. Nie nadpisywać `charge`. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 16.0 na kolejce. Następny: `/plaster` 16.0 (nie nowa rozmowa w `/noc`).
