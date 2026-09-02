# Bieżący focus

**Faza:** Fala 4 — komunikacja  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **24.0** M-31 `response_comparison` przy `quotation` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 25.0 M-32 `mail_integration` (`/plaster`). Tablica znanych adresów na `/mail`. Nie IMAP. Nie tabela skrzynki.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 4.

**Spec (jedna na sesję):** [docs/spec/mail-integration.md](../spec/mail-integration.md) — nie otwieraj `response-comparison.md` jako kolejki 25.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 25.0 odczyt domen i kontaktów, nie skrzynka, nie sekrety. Nie nadpisywać `charge`. HITL zostaje. ExtractionService nie importuje parties. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 25.0 na kolejce. Następny: `/plaster` 25.0 (nie nowa rozmowa w `/noc`).
