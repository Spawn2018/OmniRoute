# Bieżący focus

**Faza:** kolejka Q6 — towary niebezpieczne  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **6.0** M-23 `nbp_rate` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **7.0** M-52 `dangerous_good` ([delta](../deltas/open/7.0-dangerous-good.md)). Nie Fala 2.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q6.

**Spec (jedna na sesję):** [docs/spec/dangerous-good.md](../spec/dangerous-good.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 6.0 na origin. Q6 = plaster 7.0 katalog UN/IMDG. Nie podpinać wyceny. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje rates ani parties ani commodity_codes ani nbp_rates ani dangerous_goods. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 7.0 delta na origin. Następny: `/plaster` 7.0 (nie nowa rozmowa w `/noc`).
