# Bieżący focus

**Faza:** Fala 3 — ofertowanie  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **19.0** M-26 `offer_document` przy `quotation` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 20.0 M-27 Wycena wsadowa (`/plan-modul`). Nie zgaduj schematu.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 3.

**Spec (jedna na sesję):** brak — `/plan-modul` pisze. Nie otwieraj `offer-document.md` jako kolejki 20.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 19.0 podgląd dokumentu z pól wyceny, nie PDF, nie druk B/L. Nie nadpisywać `charge`. HITL zostaje. ExtractionService nie importuje quotations. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 19.0 na origin. Następny: `/plan-modul` 20.0 M-27 (nie zgaduj schematu).
