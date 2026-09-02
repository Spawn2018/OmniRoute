# Bieżący focus

**Faza:** Fala 3 — ofertowanie  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **20.0** M-27 `quotation_batch` przy `quotation` (zarchiwizowany)  
**Etap:** Plan  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** 21.0 M-28 `customer_inquiry` (`/plaster`). Ślad wycen per party. Nie tabela. Nie IMAP.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 3.

**Spec (jedna na sesję):** [docs/spec/customer-inquiry.md](../spec/customer-inquiry.md) — nie otwieraj `quotation-batch.md` jako kolejki 21.0.

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 21.0 grupuje istniejące wyceny po kontrahencie, nie nowy RFQ, nie skrzynka. Nie nadpisywać `charge`. HITL zostaje. ExtractionService nie importuje quotations. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-02:** Plan 21.0 na kolejce. Następny: `/plaster` 21.0 (nie nowa rozmowa w `/noc`).
