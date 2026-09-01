# Bieżący focus

**Faza:** kolejka Q3 — pogłębienie M-21  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **5.0** M-10 `party` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **5.1** M-21 `quotation` POL/POD + `party_id` ([delta](../deltas/open/5.1-quotation-port-party.md)). Nie Q4.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q3.

**Spec (jedna na sesję):** [docs/spec/quotation.md](../spec/quotation.md). Kanon kontrahentów 5.0: [docs/spec/parties.md](../spec/parties.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** delta 5.1 zaakceptowana `/noc`. Q3 = plaster. Żywe M-07 = `rate_line`, żywe M-08 = `charge`. HITL zostaje. ExtractionService nie importuje rates ani parties. LLM nie liczy. `party_charge_override` nadal nie karmić wyceny. `kind='terminal'` nadal nie istnieje w `location`. Lookup GUS/VIES = fixture. Port/kontrahent na wycenie nie dobierają stawki.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 5.1 delta na origin. Następny: `/plaster` 5.1 (nie nowa rozmowa w `/noc`).
