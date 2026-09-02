# Bieżący focus

**Faza:** Fala 2 — M-15 Wirtualny Dyrektor Finansowy  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **14.0** M-14 `credit_review` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 15.0 M-15 VDF (`/plan-modul`). LLM nie liczy. Nie zgaduj schematu VDF.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** brak — `/plan-modul` M-15 dopiero pisze spec. Nie otwieraj `credit-review.md` jako kolejki 15.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 14.0 katalog recenzji zamknięty. Nie auto-scoring. Nie biuro HTTP. Nie nadpisywać `credit_limit` ani M-08 `charge`. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 14.0 na origin po pushu. Następny: `/plan-modul` M-15 (nie zgaduj VDF).
