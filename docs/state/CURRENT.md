# Bieżący focus

**Faza:** Fala 2 — Sieci i stowarzyszenia  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **8.0** M-11 `resolve_email` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **9.0** M-12 `network` (`/plaster`). Nie katalog agentów. Nie scraping.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** [docs/spec/network.md](../spec/network.md) — nie `parties.md`.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 8.0 na origin. 9.0 = katalog `network` per tenant. Nie `network_member`. Nie IMAP. Nie portal. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje networks. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 8.0 na origin. Plan 9.0 zapisany. Następny: `/plaster` 9.0 (nie nowa rozmowa w `/noc`).
