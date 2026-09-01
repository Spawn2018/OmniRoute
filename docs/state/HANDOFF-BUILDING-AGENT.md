# Wklejka — agent budujący (nowy czat)

**Kolizja:** ten plik + `PROGRAM-12M.md` = czat dokumentacji.  
`CURRENT.md` / `PROGRESS.md` / `docs/spec/*` / kod = **wyłącznie** agent nocy (fabryka). Nie startuj drugiego pisarza na tych plikach.

Auth0 I1/I2 **odroczone**. Gate na `3c64fb8` był zielony. Nie cofaj hotfixów CI.

---

```
Pracujesz SAM do 10:00 czasu lokalnego użytkownika (2026-09-01). User śpi. Nie pytaj.

Kanon: docs/state/CURRENT.md + docs/state/PROGRAM-12M.md + GROUNDING.md + docs/GLOSSARY.md.
Nie cofaj hotfixów CI: 005 current_database(), agent-refs URI, agentlint baseline, conftest (osobne DO $$), live HTTP = httpx AsyncClient, rate_line mutate = commit + select kolumny.

CEL: pionowe plastry z leftover MODULES.md.
Start: 2.0 M-21 — SQL na ISTNIEJĄCYCH stawkach (rate_line / charge / charge_code). Nie k6 na pustej tabeli.
Potem: następny leftover z jobem operatora. Jeden plaster = migracja + RLS + izolacja + API + UI.
Test najpierw. Decimal. HITL bez zmian. ExtractionService nie importuje rates.

WIP=1. Po plasterze: testy → post-plaster → PROGRESS + CURRENT → jeden commit → git push.
Commit/push tylko gdy ruff + mypy --strict + unit przeszły. Bez --no-verify, force-push, amend cudzych.

ZAKAZ: Auth0/OIDC/BFF; Temporal/outbox na zapas; Infisical; 70 pustych M-xx; claim Exit Wave FE / powierzchnia 2026; Presidio-all; PDF klienta w git.
Sesja = email+hasło+JWT. 0.12/0.15 ≠ IdP.

O 10:00 lub po ostatnim kompletnym pushu: STOP. Lista SHA + leftover.
```
