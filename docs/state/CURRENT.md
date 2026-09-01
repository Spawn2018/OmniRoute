# Bieżący focus

**Faza:** Fala 2 — Automatyczne kontakty  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **7.0** M-52 `dangerous_good` (zarchiwizowany)  
**Etap:** Plaster  
**Noc:** `/noc <godzina>` (np. `/noc 7` = pętla do 7:00 czasu polskiego). Umowa: [nocna-zmiana.md](../ops/nocna-zmiana.md). Przed startem: `scripts/noc-preflight.ps1`.  
**Następny:** **8.0** M-11 `resolve_email` ([delta](../deltas/open/8.0-party-email-match.md)). Nie Fala 8.  
M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim. Leftovery UI ADR-0003 **nie** zamiast Fali 2.

**Spec (jedna na sesję):** [docs/spec/parties.md](../spec/parties.md)

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 7.0 na origin. Fala 2 = matcher maila na `party_email_domain` (5.0). Nie nowa tabela. Nie auto-INSERT kontaktu. Nie IMAP. Nie nadpisywać M-08 `charge`. HITL zostaje. ExtractionService nie importuje parties. LLM nie liczy.

**Środowisko lokalne:** `just`, `lint-imports`, `psql`, `pg_ctl` są w PATH. Przed pracą podnieś dwie rzeczy: `pg_ctl -D tools\pgdata -o "-p 5432" start` oraz `tools\openfga\openfga.exe run`. Potem `just gate` i `just test` działają bez ustawiania zmiennych. PG 16 to klaster przenośny w `tools/pg16` — instalator EDB przez winget nie przechodzi (exit 1).

**2026-09-01:** 8.0 delta na origin. Następny: `/plaster` 8.0 (nie nowa rozmowa w `/noc`).
