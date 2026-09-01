# Bieżący focus

**Faza:** Fala 2 — Sieci i stowarzyszenia  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **9.0** M-12 `network` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 10.0 M-13 `party_scorecard` (`/plaster`). Nie Fala 8. Nie zgaduj zakresu.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** [docs/spec/party-scorecard.md](../spec/party-scorecard.md) — nie otwieraj `network.md` ani `parties.md` jako kolejki 10.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 9.0 na origin (CI green). Delta 10.0 otwarta. Snapshot karty, nie silnik RFQ, nie scoring osoby. Nie IMAP. Nie portal. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje parties. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 10.0 na kolejce. Następny: `/plaster` 10.0 (nie nowa rozmowa w `/noc`).
