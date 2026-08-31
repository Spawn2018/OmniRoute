# Program 12 miesięcy — SoT agenta

**Git = kanon.** Canvas w Cursorze (`omniroute-12m-plan`) jest nawigacją, **nie** SoT.  
**Data:** 2026-08-31. **Cel:** SaaS wielodostępny pod umową, praktyki ~4.4 (nie 5.0).  
**Horyzont 12m** = reguły i anti-cele, nie „czekaj rok na moduły”.

---

## Wklejka (blok systemowy)

```
WIP=1. Max 12 plików. Test najpierw. Schemat = MCP Postgres (brak = stop).
Nie czytaj Informacje z claude/. Nie twórz Temporal/Hatchet/outbox na zapas,
Infisical, 70 pustych M-xx, haseł + Auth0 naraz.
JWT hello ≠ IdP. echo ≠ DoD. Accept HITL ≠ rate_line aż 1.3.
1.3 = ta sama transakcja HTTP, orchestracja API, nie ExtractionService, nie outbox.
Po plasterze: docs/ops/post-plaster.md + push + nowa rozmowa.
```

---

## Override CURRENT

`CURRENT.md` / `PLAN-REALIZACJA.md` / `docs-debt.md` mogą jeszcze mówić „następny = OAuth”. **Nadpisane.**

| Teraz (git) | Po zamknięciu WIP | Nie wolno |
|---|---|---|
| **Ostatni:** 0.15 hasła + refresh (archived) | **D0** → **0.15 T0** (`document_base64` max_length) | Start OAuth/OIDC |
| WIP czysty po pushu 0.15 | D0 nie miesza się z T0 | Dwa agenty na tych samych plikach |

**Kolizja numeru:** WIP **0.15 hasła** ≠ kanon **0.15 T0**. Po zamknięciu hasła zostają 0.15 w PROGRESS; T0 zostaje **0.15 T0** w tym pliku.

**OAuth** = Auth0 **I1 po Wave A**, nie skasowany leftover.

---

## Standing rules (na zawsze, też po powrocie do MODULES)

1. `organization_id` + RLS + test izolacji. Runtime: rola `omniroute_app` **NOBYPASSRLS** (nie superuser).
2. Auth produkcyjny = **Auth0 BFF + cookie httpOnly** (Code + PKCE). Hello HS256 = local/CI. Nie hasła jako produkt IdP.
3. Sekrety: **GitHub Encrypted Secrets** + `.env` w gitignore. **Zakaz Infisical.** JWT/AUTH0 nie w YAML.
4. GitHub **Pro później**. Branch protection = procedura + hooki, nie required check UI.
5. Kwoty: **Decimal / Numeric**, komponent `<Money/>`. LLM **nie liczy**.
6. **charge** = jedyna prawda o marży (kupno+sprzedaż na jednym rekordzie). **rate_line** niemutowalna + `source_ref`.
7. Accept HITL → `rate_line` przez **orchestrację API** (ten sam request/transakcja). `ExtractionService` **nie** importuje rates.
8. PDF HITL w zakresie (viewer + spany, lazy pdf.js, gzip initial ≤250 kB). Nie teatr OCR.
9. Paleta ⌘K = **akcje operatora** (extract, clear session, save view), nie sam skok po trasach.
10. Ewaluacje AI = **syntetyki** (8–12 fixture). Zero PDF klienta w git.
11. Temporal / Hatchet / outbox **zakazane**, dopóki nie ma realnego zdarzenia async **między** BC poza HTTP.
12. `Informacje z claude/` zostaje na dysku. Cursor: `.cursorignore` + zagnieżdżone `AGENTS.md` → `AGENTS.ARCHIVE.md`. Nie dumpuj do nowych docs.
13. Echo recipe ≠ DoD. `can_*` ≠ `member`. Recenzent ≠ każdy member.
14. **Zakaz 70 pustych stubów** / `module-factory` na cały rejestr. Moduł = pionowy plaster z RLS+UI, nie szkielet.
15. Każdy endpoint: jawne uprawnienie OpenFGA. Brak = deny.

---

## Wave A — zrób to, potem wróć do fabryki modułów

**Exit Wave A** = D0 **oraz** 0.15 T0 … 0.23 (T0–T5, rola RLS, HTTP+PG, hello off, reviewer≠member, sekrety poza YAML).

**Nie czekasz 12 miesięcy.** Po exicie wracasz do pierwotnego planu (`MODULES.md` / leftover produktu), **pod standing rules**. Charge 0.25–1.3 i Auth0 I1/I2 **mogą** iść równolegle z kodem produktu, jeśli pliki rozłączne.

---

## Plastry — kolejność (WIP=1)

Najpierw **0.15 hasła jest DONE** (po pushu). Potem:

| ID | Co | Spec | Zabija |
|---|---|---|---|
| **D0** | Honesty OS: AGENTS dziś/później, `.cursorignore` dump, nested AGENTS → ARCHIVE, leftover≠DONE, HC status | *brak spec produktu* | overclaim Infisical/Temporal |
| **0.15 T0** | `document_base64` `max_length` → 422 przed decode | `extraction.md` | DoS |
| **0.16 T1** | Rola `omniroute_app` NOBYPASSRLS | `tenancy.md` | superuser omija RLS |
| **0.17 T2** | Matryca izolacji S1–S6 + WITH CHECK | `tenancy.md` | luki SQL |
| **0.18** | HTTP extract na żywej PG; token A / draft B → 404 | `extraction.md` | stub serwisu jako „HTTP done” |
| **0.19 A1** | Undeclared `/api/v1` = deny; playground off | — | HC-05 konwencja |
| **0.20 A2** | `can_review` = reviewer, nie member | OpenFGA | każdy member = admin |
| **0.21 T4** | `hello_token` default **false** (ON tylko local+CI) | `tenancy.md` | mint UUID na sieci |
| **0.22 T5** | iss/aud/jti, TTL 15 min, `token_version` | `tenancy.md` | goły HMAC |
| **0.23 S1** | `JWT_SECRET` z GitHub Encrypted Secrets, nie YAML | ops | literał w CI |

**Fork po Wave A** (max 3 agenty; pliki ∩ = ∅; **nie** `rate_line` ∥ insert w `accept` w tym samym tygodniu):

| Tor | ID | Co | Zakaz równoległy |
|---|---|---|---|
| Charge | 0.24 | pip-audit, pin SHA, `/ready`, request-id (opcjonalnie tu) | — |
| Charge | 0.25 | Money Decimal + `<Money/>` | float |
| Charge | 1.0 | `charge_code` M-06 | luźny string |
| Charge | 1.1 | `rate_line` immutable + `source_ref` | pusta domena |
| Charge | 1.2 | `charge` buy+sell, marża w kodzie | marża poza charge |
| Charge | 1.3 | accept → RatesService, jedna transakcja HTTP | accept w próżnię; outbox |
| FE | U0–U3 | adapter, shell, tabela ADR, HITL; PDF lazy w U3/4.4 | ręczny `frontend/src/api` |
| FE | U4–U7 | paleta akcji, RTL, size-limit fail | — |
| Auth0 | **I1** | BFF + PKCE + cookie; org z `app_metadata`; first-login bez org = odmowa | hasła + Auth0; auto-create org |
| Auth0 | I2 | RS256 JWKS; hello OFF staging/prod | nowy HS256 |
| AI leftover | 2.1–2.2 | Presidio **tylko** instructor stub; 8–12 syntetyk | 30 PDF klienta; Presidio-all |
| Q4 | 2.0 | M-21 SQL **tylko** jeśli są stawki | k6 na pustej tabeli |

Auth0: SPA Vite → BFF FastAPI → Auth0. Cookie HttpOnly; Secure; SameSite=Lax. OpenFGA = SoT ról (first-login = member; reviewer ręczny seed). Region EU jeśli plan pozwala. Organizations feature **nie** w I1.

---

## Anti-cele (odmów)

Temporal/Hatchet/outbox na zapas · Infisical · 70 pustych M-xx · k6 50k · OTel-sprint · `just perf` echo jako DoD · Presidio na każdym endpoincie · żywy OpenAI w gate · `can_*` = member · accept bez HITL · hasła+Auth0 w jednym plasterze · persony `.cursor/agents/` · dump Claude w kontekście · zmiana starych migracji · Next.js · pgvector „bo stos” · required checks na Free · twierdzenie że 0.12 = IdP · OCR-teatr zamiast viewer+spans.

**Nie pytaj ponownie:** IdP, Infisical, PDF w zakresie, Temporal, Pro, dump, paleta, horyzont, eval PDF klienta, kolejność charge vs leftover AI.

---

## Kolizje plików (max 3 agenty / tydzień)

| Tor | WIP | Zakaz |
|---|---|---|
| A Backend | 1 plaster | drugi BE; `accept` insert **i** `rate_line` w tym samym tygodniu |
| B Frontend | 1, pliki ∩ A = ∅ | ręczny `frontend/src/api`; regen OpenAPI w locie A |
| C Docs/OS | D0 / honesty | `CURRENT` / `PROGRESS` / aktywna delta = zamykający Code |
| D Review | po PR, `pr-review` | pisać kod |
| E CURRENT | jeden pisarz | dwa agenty na `CURRENT.md` |

**Semantyka:** I1 Auth0 + wypełnienie U0 = **jeden** plaster pionowy. 1.3 + zmiana copy HITL = jeden plaster. Charge ∥ Auth0 OK gdy `session*` ≠ `rate*` / `charge*` / `extraction*`.

---

## Skills

Obowiązkowe: `nowy-plaster`, `zamknij-plaster`, `lowca-duplikatow` (przed kodem), `migracja-rls`, `openfga-change` (gdy model FGA), `ekstraktor` (granica accept), `pr-review`, `knowledge-retrieve` ≤8 kart.

**Nie:** `module-factory` na 70 BC.

Po D0: pętla `docs/ops/post-plaster.md`. Nie edytuj AGENTS / `.cursorignore` poza D0.
