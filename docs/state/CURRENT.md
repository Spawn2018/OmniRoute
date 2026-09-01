# Bieżący focus

**Faza:** kolejka Q5 — waluty i kurs NBP  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **5.2** M-09 `commodity_code` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **Q5** waluty i kurs NBP (archiwum M-07; **nie** nadpisuj żywego M-07 `rate_line`). Nie Q6.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q5.

**Spec (jedna na sesję):** brak do `/plan-modul` — żywy ID nadajesz w Planie.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 5.2 na origin. Q5 = Plan walut/NBP. Nie drugi silnik stawek. Żywe M-07 = `rate_line`, żywe M-08 = `charge`. HITL zostaje. ExtractionService nie importuje rates ani parties ani commodity_codes. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 5.2 na origin. Następny: `/plan-modul` Q5 (nie nowa rozmowa w `/noc`).
