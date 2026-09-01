# Bieżący focus

**Faza:** kolejka Q6 — towary niebezpieczne  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **6.0** M-23 `nbp_rate` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** Q6 Plan (`/plan-modul`) — towary niebezpieczne (archiwum M-08; **nie** nadpisuj żywego M-08 `charge`).  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q6.

**Spec (jedna na sesję):** brak — najpierw delta Q6.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 6.0 na origin. Q6 = Plan, nie plaster. Nie nadpisywać żywego M-08 `charge`. HITL zostaje. ExtractionService nie importuje rates ani parties ani commodity_codes ani nbp_rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 6.0 na origin. Następny: `/plan-modul` Q6 (nie nowa rozmowa w `/noc`).
