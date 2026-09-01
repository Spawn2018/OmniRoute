# Bieżący focus

**Faza:** kolejka Q2 — M-10 Kontrahenci  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **4.2** M-05 `terminal` + WPI (zarchiwizowany)  
**Etap:** Agent — delta 5.0 zaakceptowana; kod tylko w nowej rozmowie `/plaster`.  
**Następny:** **5.0** M-10 `party` (`docs/deltas/open/5.0-party.md`). Nie Q3.  
Q3 = pogłębienie żywego M-21 **po** 5.0. M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast 5.0. `operator_party_id` na terminalu = ten plaster.

**Spec (jedna na sesję):** [docs/spec/parties.md](../spec/parties.md). Kanon geografii 4.0–4.2: [docs/spec/geography.md](../spec/geography.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 4.2 na origin. Q1 M-05 zamknięte. Plan Q2 zaakceptowany: cały katalog M-10 w 5.0 (`party` + kontakty, rachunki, domeny, override, `carrier_profile`, lookup GUS/VIES/whitelist jako szkic). Żywe M-07 = `rate_line`, żywe M-08 = `charge` — nie nadpisuj numerami archiwum. HITL zostaje. ExtractionService nie importuje rates ani parties. LLM nie liczy. `party_charge_override` nie karmić wyceny. Operator terminalu w kodzie nadal tekstem aż `/plaster`. `kind='terminal'` nadal nie istnieje w `location`. WPI = kolumny na `port`, ingest poza HTTP.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools\pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** Plan 5.0 — delta otwarta, spec szkielet. Zero kodu produktu w rozmowie Plan. Następny: nowa rozmowa Agent + `/plaster`.
