# Wklejka — agent budujący (nowy czat albo Cloud)

**Kanon planu = [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md).**  
Noc: [docs/ops/nocna-zmiana.md](../ops/nocna-zmiana.md). `PROGRAM-12M.md` = alias, nie SoT.

Auth0 I1/I2 **odroczone**. Nie cofaj hotfixów CI.

---

```
Kanon: docs/PLAN-REALIZACJA.md + docs/state/CURRENT.md + GROUNDING.md + docs/GLOSSARY.md.
Noc: docs/ops/nocna-zmiana.md (jeden plaster kodu; Plan = opcja rekomendowana).
Nie cofaj hotfixów CI: 005 current_database(), agent-refs URI, agentlint baseline,
conftest (osobne DO $$), live HTTP = httpx AsyncClient, rate_line mutate = commit + select kolumny.

Następny = 4.1 M-05 location + strefy. Delta docs/deltas/open/4.1-location-zones.md.
Komenda /plaster (tryb Agent), potem /testy (czerwone), potem kod, potem /zamknij.
Nie 4.2. Nie Q2. M-02 parked. Auth0 odroczone. Exit Wave FE nie claim.

WIP=1. Po 4.1: CURRENT = Plan 4.2 (Q1.2), nie kod 4.2 tej samej nocy.
Test najpierw. Decimal. HITL bez zmian. ExtractionService nie importuje rates.
Cloud: branch + PR, nie force na main. Lokalnie: hook scripts/githooks, bez --no-verify.

ZAKAZ: Auth0/OIDC/BFF; Temporal/outbox na zapas; Infisical; 70 pustych M-xx;
claim Exit Wave FE / powierzchnia 2026; Presidio-all; PDF klienta w git.
```
