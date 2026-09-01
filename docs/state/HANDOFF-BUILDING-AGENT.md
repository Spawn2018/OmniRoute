# Wklejka — agent budujący (nowy czat albo noc)

**Kanon planu = [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md).**  
Noc: [docs/ops/nocna-zmiana.md](../ops/nocna-zmiana.md) — komenda `/noc 7` (godzina = koniec pętli). `PROGRAM-12M.md` = alias, nie SoT.

Auth0 I1/I2 **odroczone**. Nie cofaj hotfixów CI. Kolejny plaster **zawsze** z `docs/state/CURRENT.md`, nie z tej wklejki.

---

```
Kanon: docs/PLAN-REALIZACJA.md + docs/state/CURRENT.md + GROUNDING.md + docs/GLOSSARY.md.
Noc: /noc 7 (pętla do 7:00 Europe/Warsaw). Umowa docs/ops/nocna-zmiana.md.
Przed startem: powershell -ExecutionPolicy Bypass -File scripts/noc-preflight.ps1
Nie cofaj hotfixów CI: 005 current_database(), agent-refs URI, agentlint baseline,
conftest (osobne DO $$), live HTTP = httpx AsyncClient, rate_line mutate = commit + select kolumny.

Czytaj CURRENT — nie zgaduj numeru plastra.
Plan w Agencie (nie tryb Plan w Cursorze) + push; plaster: testy czerwone, kod, push.
Naprawiaj do skutku. Po godzinie: raport dla laika, nie nowy plan.
M-02 parked. Auth0 odroczone. Exit Wave FE nie claim.

WIP=1 w danym cyklu. Decimal. HITL bez zmian. ExtractionService nie importuje rates.
Push na origin/main, hook scripts/githooks, bez --no-verify, bez force.

ZAKAZ: Auth0/OIDC/BFF; Temporal/outbox na zapas; Infisical; 70 pustych M-xx;
claim Exit Wave FE / powierzchnia 2026; Presidio-all; PDF klienta w git.
```
