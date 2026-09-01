# Bieżący focus

**Faza:** Fala 2 — Sieci i stowarzyszenia  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **11.0** M-16 `customer_sop` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** M-18 Opłaty portowe warunkowe (`/plan-modul`). Nie Fala 8. Nie zgaduj zakresu.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** brak — Plan M-18 pisze spec. Nie otwieraj `customer-sop.md` ani `party-scorecard.md` jako kolejki.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 11.0 na origin po pushu. Katalog SOP + zatwierdzenie, nie generator zadań, nie M-35. Nie IMAP. Nie portal. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje parties. LLM nie liczy i nie pisze SOP.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 11.0 zamknięty. Następny: `/plan-modul` M-18 (nie nowa rozmowa w `/noc`).
