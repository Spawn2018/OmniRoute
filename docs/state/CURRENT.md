# Bieżący focus

**Faza:** kolejka Q1 — M-05 Geografia, pozycja **4.2** `terminal` + WPI  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **4.1** M-05 `location` + strefy taryfowe (zarchiwizowany)  
**Etap:** **Plan** — brak delty dla 4.2. Najpierw tryb Plan i `/plan-modul`, zero kodu.  
**Następny:** **4.2** M-05 `terminal` (ISPS, operator jako tekst) + pola World Port Index na `port`. Spec: `docs/spec/geography.md`. Nie Q2.  
Q2 = M-10 **po** 4.2. M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast 4.2.

**Spec (jedna na sesję):** [docs/spec/geography.md](../spec/geography.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 4.1 na origin. Żywe M-07 = `rate_line`, żywe M-08 = `charge` — nie nadpisuj numerami archiwum M-07/M-08. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy. `location.organization_id` i `port.organization_id` obowiązkowe. Nakładanie zakresów pocztowych blokuje baza (`ex_zone_member_no_overlap`), nie walidacja w serwisie — nie przenoś tego do Pythona. `resolve` strefy dopasowuje kod dokładnej długości; `pg_trgm` i geometria poligonowa nadal poza zakresem. `kind='terminal'` **nie istnieje** w `location` — terminal to osobna tabela w 4.2.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 4.1 zamknięte — `location`, `location_zone_member`, typ `postal_range` z kolacją `"C"`, kolumna generowana `postal_span`, exclusion GiST, RLS FORCE na obu tabelach, `/locations`. Migracja `013_location_rls` dokłada też `uq_port_org_id` na `port` — 4.0 zostawiło tylko unikat po `unlocode`, a FK złożone potrzebowało nośnika. Schemat testowy powstaje z `create_all`, więc typ, kolumna generowana i exclusion są odtwarzane w `backend/tests/conftest.py` obok polityk RLS. OpenFGA bez zmian: `can_manage_geography`.
