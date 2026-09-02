# Bieżący focus

**Faza:** Fala 4 — komunikacja  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **26.0** M-33 `mail_client` `mailto:` na `/mail` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 27.0 M-34 Powiadomienia (`/plan-modul`). Nie zgaduj schematu.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 4.

**Spec (jedna na sesję):** brak — `/plan-modul` pisze. Nie otwieraj `mail-client.md` jako kolejki 27.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 26.0 `mailto:` z katalogu kontaktów, nie dodatek Outlook, nie sekrety. Nie nadpisywać `charge`. HITL zostaje. ExtractionService nie importuje parties. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 26.0 na origin. Następny: `/plan-modul` 27.0 M-34 (nie zgaduj schematu).
