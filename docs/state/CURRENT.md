# Bieżący focus

**Faza:** kolejka Q5 — waluty i kurs NBP  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **5.2** M-09 `commodity_code` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **6.0** M-23 `nbp_rate` ([delta](../deltas/open/6.0-nbp-rate.md)). Nie Q6.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q5.

**Spec (jedna na sesję):** [docs/spec/nbp-rate.md](../spec/nbp-rate.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 5.2 na origin. Q5 = plaster 6.0 katalog kursu. Nie przeliczać wyceny. Nie nadpisywać M-07 `rate_line`. Żywe M-08 = `charge`. HITL zostaje. ExtractionService nie importuje rates ani parties ani commodity_codes ani nbp_rates. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 6.0 delta na origin. Następny: `/plaster` 6.0 (nie nowa rozmowa w `/noc`).
