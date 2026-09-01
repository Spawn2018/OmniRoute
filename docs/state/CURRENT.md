# Bieżący focus

**Faza:** Fala 2 — po katalogach F2.0–F2.5; dalej M-14  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **13.0** M-19 `channel_quote` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** `/plan-modul` M-14 ocena kredytowa (zakaz auto-scoringu `natural_person` / JDG). Nie Fala 8. Nie zgaduj zakresu.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** brak do planu M-14 — nie otwieraj `channel-quote.md` jako kolejki.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 13.0 katalog oferty z kanału, nie live HTTP, nie zapis do `rate_line`/`charge`. Nie IMAP. Nie portal. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 13.0 zamknięty. Następny: `/plan-modul` M-14.
