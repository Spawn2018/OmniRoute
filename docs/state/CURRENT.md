# Bieżący focus

**Faza:** Fala 5 — zlecenie  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **27.0** M-34 `operator_notice` tablica `/notifications` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 28.0 M-35 `shipment` (`/plaster`). Tablica wycen z `party_id`. Nie tabela. Nie tracking.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 5.

**Spec (jedna na sesję):** [docs/spec/shipment.md](../spec/shipment.md) — nie otwieraj `operator-notice.md` jako kolejki 28.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 28.0 odczyt wycen, nie tabela `shipment`. Nie zgaduj HBL / odcinków. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 28.0 na kolejce. Następny: `/plaster` 28.0 (nie nowa rozmowa w `/noc`).
