# Bieżący focus

**Faza:** kolejka Q1 — M-05 Geografia, pozycja **4.1** `location` + strefy  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **4.0** M-05 `port` (zarchiwizowany)  
**Etap:** **Plan** (brak delty 4.1). Nowa rozmowa, tryb Plan + `/plan-modul`. Zero kodu.  
**Następny:** **4.1** M-05 `location` + strefy (`location_zone_member`). Spec: `docs/spec/geography.md`. Nie 4.2. Nie Q2.  
Q1.2 = 4.2 `terminal`+WPI (też najpierw Plan). Q2 = M-10 **po** 4.2. M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast 4.1.

**Spec (jedna na sesję):** [docs/spec/geography.md](../spec/geography.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 4.0 na origin. Żywe M-07 = `rate_line`, żywe M-08 = `charge` — nie nadpisuj numerami archiwum M-07/M-08. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy. `port.organization_id` obowiązkowy. `resolve` portu dopasowuje kod albo alias dokładnie — `pg_trgm` nadal poza zakresem.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 4.0 zamknięte — `port`, RLS, `resolve`, `/ports`. Następne: Plan 4.1.
