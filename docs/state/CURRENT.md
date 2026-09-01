# Bieżący focus

**Faza:** kolejka Q4 — kody towarowe  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **5.1** M-21 `quotation` POL/POD + `party_id` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **5.2** M-09 `commodity_code` ([delta](../deltas/open/5.2-commodity-code.md)). Nie Q5.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q4.

**Spec (jedna na sesję):** [docs/spec/commodity-code.md](../spec/commodity-code.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 5.1 na origin. Q4 = plaster 5.2 katalog. Nie podpinać kodu do wyceny. Nie Q6 IMDG. Żywe M-07 = `rate_line`, żywe M-08 = `charge`. HITL zostaje. ExtractionService nie importuje rates ani parties ani commodity_codes. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 5.2 delta na origin. Następny: `/plaster` 5.2 (nie nowa rozmowa w `/noc`).
