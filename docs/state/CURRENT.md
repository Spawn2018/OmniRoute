# Bieżący focus

**Faza:** Wave FE leftover (po Fali 11)  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **54.0** U-primitives-json pin Radix w `components.json` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** U-i18n-structure (`/plan-modul`). PLAN § Wave FE leftover. Nie zgaduj schematu. Nie nowa tabela.  
M-02 **parked**. Auth0 **odroczone**. Portale **parked**. Exit Wave FE **nie** claim.

**Spec (jedna na sesję):** brak do `/plan-modul` — nie otwieraj [shadcn-radix-base.md](../spec/shadcn-radix-base.md) jako kolejki U-i18n-structure.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** nie licz kwot w JS. HITL zostaje. LLM nie liczy. `charge` zostaje prawdą o marży. ExtractionService nie importuje quotations.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** 54.0 na kolejce zamknięcia. Następny: `/plan-modul` U-i18n-structure (nie nowa rozmowa w `/noc`).
