# Bieżący focus

**Faza:** kolejka Q2 — M-10 Kontrahenci  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **4.2** M-05 `terminal` + WPI (zarchiwizowany)  
**Etap:** Plan — wydmuszka Q2, zero kodu do `/plan-modul`.  
**Następny:** **Q2** M-10 Kontrahenci. Archiwum M-10; żywy ID nadajesz w Planie. Nie Q3.  
Q3 = pogłębienie żywego M-21 **po** Q2. M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Q2. `operator_party_id` na terminalu = ten Q, nie 4.2.

**Spec (jedna na sesję):** brak — powstaje w `/plan-modul`. Kanon geografii 4.0–4.2: [docs/spec/geography.md](../spec/geography.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 4.2 na origin. Q1 M-05 zamknięte (`port` / `location` / `terminal` + WPI). Żywe M-07 = `rate_line`, żywe M-08 = `charge` — nie nadpisuj numerami archiwum. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy. `terminal.organization_id` obowiązkowe. Operator terminalu zostaje tekstem aż Plan Q2 da `party`. `kind='terminal'` nadal nie istnieje w `location`. WPI = kolumny na `port`, ingest poza HTTP.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 4.2 zamknięte — tabela `terminal` (ISPS, `operator_name` tekst, RLS FORCE, unikat częściowy kodu, FK złożone do `port`), kolumny World Port Index na `port`, ingest `scripts/seed_wpi.py` + fixture CI, `/terminals` i kolumny WPI na `/ports`. OpenFGA bez zmian: `can_manage_geography`. Migracja `014_terminal_rls`.
