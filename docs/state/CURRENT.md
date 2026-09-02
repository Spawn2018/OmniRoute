# Bieżący focus

**Faza:** Fala 2 — M-14 ocena kredytowa  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **13.0** M-19 `channel_quote` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 14.0 M-14 `credit_review` (`/plaster`). Nie Fala 8. Nie zgaduj auto-scoringu.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** [docs/spec/credit-review.md](../spec/credit-review.md) — nie otwieraj `channel-quote.md` ani `party-scorecard.md` jako kolejki 14.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 14.0 katalog recenzji, nie auto-scoring `natural_person` / JDG, nie zmiana `credit_limit`. Nie biuro HTTP. Nie portal. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 14.0 na kolejce. Następny: `/plaster` 14.0 (nie nowa rozmowa w `/noc`).
