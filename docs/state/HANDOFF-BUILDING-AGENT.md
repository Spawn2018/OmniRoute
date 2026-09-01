# Wklejka — agent budujący (nowy czat)

**Kanon planu = [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md).**  
`PROGRAM-12M.md` = alias + stara wklejka, nie SoT. Ten plik = historyczna wklejka nocnego agenta, nie drugi pisarz na kod. Czat scalający docs (2026-09-01) **nie** jest drugim building agentem.

Auth0 I1/I2 **odroczone**. HEAD `8fb8c93` (3.0) — gate zielony. Nie cofaj hotfixów CI.

---

```
Kanon: docs/PLAN-REALIZACJA.md + docs/state/CURRENT.md + GROUNDING.md + docs/GLOSSARY.md.
Nie cofaj hotfixów CI: 005 current_database(), agent-refs URI, agentlint baseline,
conftest (osobne DO $$), live HTTP = httpx AsyncClient, rate_line mutate = commit + select kolumny.

Następny = 4.0 M-05 `port`. Komenda `/plaster` (tryb Agent), delta `docs/deltas/open/4.0-port.md`.
Nie 4.1/4.2. Nie Q2. M-02 parked. Auth0 I1/I2 odroczone (brak tenanta).
Exit Wave FE nie claim. Sesja = email+hasło+JWT. 0.12/0.15 ≠ IdP.

WIP=1. Po plasterze 4.0: CURRENT = Q1.1 Plan 4.1, nie Q2.
Test najpierw. Decimal. HITL bez zmian. ExtractionService nie importuje rates.
Po plasterze: post-plaster → PROGRESS + CURRENT → commit → push → nowa rozmowa.

ZAKAZ: Auth0/OIDC/BFF; Temporal/outbox na zapas; Infisical; 70 pustych M-xx;
claim Exit Wave FE / powierzchnia 2026; Presidio-all; PDF klienta w git.
```
