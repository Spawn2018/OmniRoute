# Program 12 miesięcy — SoT agenta

**Git = kanon.** Canvas w Cursorze (`omniroute-12m-plan`) jest nawigacją, **nie** SoT.  
**Data:** 2026-09-01 (pasek FE 2026 zablokowany). **Cel:** SaaS wielodostępny pod umową, praktyki ~4.4 (nie 5.0).  
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
| **Ostatni:** 0.24 | **2.1–2.2** Presidio instructor stub + 8–12 syntetyk. Auth0 I1/I2 **odroczone** | Start I1/I2 bez tenanta Auth0 |
| WIP czysty po pushu 0.24 | max 3 agenty; pliki ∩ = ∅ | Dwa agenty na tych samych plikach |

**Kolizja numeru:** WIP **0.15 hasła** ≠ kanon **0.15 T0**. Po zamknięciu hasła zostają 0.15 w PROGRESS; T0 zostaje **0.15 T0** w tym pliku.

**OAuth** = Auth0 I1/I2 **odroczone** (brak tenanta). Nie pytać aż user ma tenant. Sesja = email+hasło+JWT. 0.12/0.15 **nie** są IdP.

---

## Standing rules (na zawsze, też po powrocie do MODULES)

1. `organization_id` + RLS + test izolacji. Runtime: rola `omniroute_app` **NOBYPASSRLS** (nie superuser).
2. Auth produkcyjny **gdy będzie tenant** = Auth0 BFF + cookie httpOnly (Code + PKCE). **I1/I2 nie teraz** — brak tenanta; nie pytać aż user go ma. Sesja dziś = email+hasło+JWT (0.15 + 0.12). Hello HS256 = local/CI. 0.12/0.15 **nie** są IdP.
3. Sekrety: **GitHub Encrypted Secrets** + `.env` w gitignore. **Zakaz Infisical.** JWT/AUTH0 nie w YAML.
4. GitHub **Pro później**. Branch protection = procedura + hooki, nie required check UI.
5. Kwoty: **Decimal / Numeric**, komponent `<Money/>`. LLM **nie liczy**.
6. **charge** = jedyna prawda o marży (kupno+sprzedaż na jednym rekordzie). **rate_line** niemutowalna + `source_ref`.
7. Accept HITL → `rate_line` przez **orchestrację API** (ten sam request/transakcja). `ExtractionService` **nie** importuje rates.
8. PDF HITL w zakresie (viewer + spany, lazy pdf.js, gzip initial ≤250 kB) = **U-pdf-spans**. Nie teatr OCR.
9. Paleta ⌘K = **akcje operatora** (extract, accept-focus, save view, clear session) = **U-palette-ops**, nie sam skok po trasach.
10. Ewaluacje AI = **syntetyki** (8–12 fixture). Zero PDF klienta w git.
11. Temporal / Hatchet / outbox **zakazane**, dopóki nie ma realnego zdarzenia async **między** BC poza HTTP.
12. `Informacje z claude/` zostaje na dysku. Cursor: `.cursorignore` + zagnieżdżone `AGENTS.md` → `AGENTS.ARCHIVE.md`. Nie dumpuj do nowych docs.
13. Echo recipe ≠ DoD. `can_*` ≠ `member`. Recenzent ≠ każdy member.
14. **Zakaz 70 pustych stubów** / `module-factory` na cały rejestr. Moduł = pionowy plaster z RLS+UI, nie szkielet.
15. Każdy endpoint: jawne uprawnienie OpenFGA. Brak = deny.
16. **Exit Wave FE** = **wszystkie** ID `U-*` w sekcji „Exit Wave FE”. Adapter OpenAPI + RTL **nie** zamyka fali. Twierdzenie „scaffold 2026 + powierzchnia 2026” **zakazane**, dopóki każdy U-* nie ma widocznego DoD i gate, który pada.

### AI Act (produkt, nie PDF prawny)

- Stan obecny (ekstrakcja HITL, brak scoringu osoby fizycznej) = **minimal risk** wg archiwum.
- **Zakaz:** automatyczny credit scoring `natural_person` / JDG (to byłby high-risk).
- Art. 50 (w mocy od 2026-08-02 wg archiwum): obowiązkowe oznaczenie treści AI w UI — plaster **U-art50**, nie notatka prawna.
- D0 **nie** zdejmuje HITL / human decision-maker / „LLM nigdy nie liczy”.
- Archiwum **nie** jest opinią prawną.

---

## Wave A — zrób to, potem wróć do fabryki modułów

**Exit Wave A** = D0 **oraz** 0.15 T0 … 0.23 (T0–T5, rola RLS, HTTP+PG, hello off, reviewer≠member, sekrety poza YAML). Wave FE **nie** jest częścią Wave A.

**Nie czekasz 12 miesięcy.** Po exicie wracasz do pierwotnego planu (`MODULES.md` / leftover produktu), **pod standing rules**. Charge 0.25–1.3, Auth0 I1/I2 i Wave FE **mogą** iść równolegle z kodem produktu **po Exit Wave A**, jeśli pliki rozłączne. Wave FE **nie** startuje przed D0/T0…0.23.

---

## Plastry — kolejność (WIP=1)

**Wave A DONE** (D0 + 0.15 T0 … 0.23 po pushu). Potem fork:

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
| Charge | 0.24 | **DONE:** pip-audit projektu, pin SHA Actions, `/ready`, request-id | — |
| Charge | 0.25 | Money Decimal + `<Money/>` | float |
| Charge | 1.0 | `charge_code` M-06 | luźny string |
| Charge | 1.1 | `rate_line` immutable + `source_ref` | pusta domena |
| Charge | 1.2 | `charge` buy+sell, marża w kodzie | marża poza charge |
| Charge | 1.3 | accept → RatesService, jedna transakcja HTTP | accept w próżnię; outbox |
| FE | U0 | OpenAPI adapter (codegen) — **nie** zamyka fali | ręczny `frontend/src/api`; regen OpenAPI w locie A |
| FE | U1 | App shell (layout, routing) — **nie** zamyka fali | 4 trasy hello = „powierzchnia 2026” |
| FE | U2 | Tabela biznesowa wg ADR-0002 (TanStack Table) | lista bez wirtualizacji gdy dane |
| FE | U-density | Compact default + density toggle na **wszystkich** listach biznesowych | gęstość tylko na users / hello-dashboard |
| FE | U-palette-ops | ⌘K = akcje operatora (standing #9) | paleta = skok po trasach |
| FE | U-pdf-spans | PDF viewer + spany HITL, lazy (standing #8) | OCR-teatr; PDF w initial bundle |
| FE | U-routes-breadth | Każdy plaster BC z jobem operatora = trasa/UI w tym samym plasterze | backend-only charge / rate_line / session |
| FE | U-a11y | Pełna ścieżka klawiatury + focus-visible | zamknięcie fali na RTL |
| FE | U-size-limit-real | `just perf` / size-limit **failuje** CI | echo jako DoD |
| FE | U-art50 | Label „propozycja AI” na draftach HITL | Art. 50 = PDF prawny zamiast UI |
| FE | U-admin-ref | Checklist vs dense shadcn-admin | U0 adapter = Exit Wave FE |
| Auth0 | **I1** | **ODROCZONE** (brak tenanta). Gdy będzie: BFF + PKCE + cookie; org z `app_metadata`; first-login bez org = odmowa | start I1 bez tenanta; hasła + Auth0; auto-create org; hello OAuth |
| Auth0 | I2 | **ODROCZONE**. Gdy będzie: RS256 JWKS; hello OFF staging/prod | start I2 bez tenanta; nowy HS256 |
| AI leftover | 2.1–2.2 | Presidio **tylko** instructor stub; 8–12 syntetyk | 30 PDF klienta; Presidio-all |
| Q4 | 2.0 | M-21 SQL **tylko** jeśli są stawki | k6 na pustej tabeli |

Auth0 I1/I2: **nie teraz**. Hasła + refresh zostają sesją. Nie pytać ponownie, dopóki user nie ma tenanta Auth0. Gdy będzie tenant: SPA Vite → BFF FastAPI → Auth0; cookie HttpOnly; Secure; SameSite=Lax; region EU / SCC jeśli plan pozwala; OpenFGA = SoT ról (first-login = member; reviewer ręczny seed). Organizations feature **nie** w I1. Zero kodu Auth0 / placeholder tenanta / „hello OAuth” do tego czasu.

Wave FE startuje **dopiero po Exit Wave A** (fork równoległy z Charge/Auth0, **nie** zamiast D0/T0). **Exit Wave FE** = wszystkie wiersze FE powyżej **oraz** tabela DoD poniżej. U0–U2 (adapter, shell, tabela) zostają jako scaffold; **nie** zastępują U-*.

---

## Exit Wave FE — powierzchnia 2026 (obowiązkowe)

**Fala NIE jest zamknięta**, dopóki **każdy** ID poniżej nie przejdzie. Pasek = software house 2026, nie 2024 hello-dashboard. Twierdzenie „scaffold 2026 + powierzchnia 2026” **zakazane** przed tym exitem.

Koszyki U0–U7 **rozbite**: U0 adapter / U1 shell / U2 tabela ADR zostają; HITL+PDF → **U-pdf-spans**; paleta → **U-palette-ops**; RTL → **U-a11y** (szersze niż RTL); size-limit → **U-size-limit-real**. Nie duplikuj pracy — nie zamykaj dwóch ID tym samym commitem „adapter + RTL”.

| ID | Co operator ZOBACZY | Gate co padnie |
|---|---|---|
| **U-density** | Domyślnie **compact** na **wszystkich** listach biznesowych (nie tylko users). Toggle density. Progressive disclosure, gęsty admin — nie kafelki hello. | Lista biznesowa bez compact / bez toggle. |
| **U-palette-ops** | ⌘K otwiera **akcje**: extract, accept-focus, save view, clear session — nie sam „idź do trasy”. | Paleta bez akcji operatora (tylko nawigacja). |
| **U-pdf-spans** | Viewer strony PDF + podświetlenia spanów na HITL. Lazy load pdf.js. | Brak highlightów; PDF w initial JS; gzip initial **> 250 kB** (budget z AGENTS.md). |
| **U-routes-breadth** | Każdy nowy plaster BC w tym programie, który ma job operatora, dostaje **trasę/UI w tym samym pionowym plasterze**. Istniejące 4 trasy hello **nie** wystarczą na claim powierzchni 2026. Po Wave A: **zakaz** backend-only „UI later” dla charge / rate_line / session. | Plaster charge/rate_line/session bez trasy; claim powierzchni na 4 hello routes. |
| **U-a11y** | Pełna ścieżka klawiatury (ADR-0002 / ui-design-system): focus-visible, operator first. RTL to **nie** DoD. | Brak focus-visible; ścieżka tylko myszą; zamknięcie fali na sam RTL. |
| **U-size-limit-real** | `just perf` / size-limit **musi failować CI** (nie `echo`). Budget AGENTS.md: JS gzip initial **< 250 kB**; wirtualizacja list p95 tam, gdzie są dane. | Recipe-echo; przekroczony 250 kB przechodzi CI. |
| **U-art50** | Na draftach HITL (teraz) i na copilot/mail (gdy polecą): widoczne **„propozycja AI”** / treść wygenerowana. Art. 50 już w mocy od 2026-08-02 wg archiwum. To plaster **produktu**, nie PDF prawny. | Draft HITL bez labelu AI; Art. 50 odłożone na „legal later”. |
| **U-admin-ref** | Exit checklist vs dense shadcn-admin: gęstość sidebara, table toolbar, command actions. | Zamknięcie Wave FE zdaniem „U3 = OpenAPI adapter” / „adapter + RTL”. |

Debt-zero na plasterze FE, RLS nietknięte od strony UI (tenancy z BE). Charge przed leftover AI — bez zmian. WIP=1, max 3 agenty/tydzień, hasła 0.15 ≠ 0.15 T0.

---

## Anti-cele (odmów)

Temporal/Hatchet/outbox na zapas · Infisical · 70 pustych M-xx · k6 50k · OTel-sprint · `just perf` echo jako DoD · Presidio na każdym endpoincie · żywy OpenAI w gate · `can_*` = member · accept bez HITL · hasła+Auth0 w jednym plasterze · persony `.cursor/agents/` · dump Claude w kontekście · zmiana starych migracji · Next.js · pgvector „bo stos” · required checks na Free · twierdzenie że 0.12 = IdP · OCR-teatr zamiast viewer+spans · zamknięcie Wave FE na adapter OpenAPI + RTL · „powierzchnia 2026” przed Exit Wave FE · auto credit scoring `natural_person` / JDG · zdejmowanie HITL w D0.

**Nie pytaj ponownie:** Auth0 I1/I2 (aż user ma tenant), IdP, Infisical, PDF w zakresie, Temporal, Pro, dump, paleta, horyzont, eval PDF klienta, kolejność charge vs leftover AI, kompromis na Exit Wave FE, „adapter wystarczy na powierzchnię 2026”, „0.12/0.15 = IdP”.

---

## Kolizje plików (max 3 agenty / tydzień)

| Tor | WIP | Zakaz |
|---|---|---|
| A Backend | 1 plaster | drugi BE; `accept` insert **i** `rate_line` w tym samym tygodniu |
| B Frontend | 1, pliki ∩ A = ∅ | ręczny `frontend/src/api`; regen OpenAPI w locie A |
| C Docs/OS | D0 / honesty | `CURRENT` / `PROGRESS` / aktywna delta = zamykający Code |
| D Review | po PR, `pr-review` | pisać kod |
| E CURRENT | jeden pisarz | dwa agenty na `CURRENT.md` |

**Semantyka:** I1 Auth0 + wypełnienie U0 (adapter) = **jeden** plaster pionowy — to **nie** jest Exit Wave FE. 1.3 + zmiana copy HITL / **U-art50** = jeden plaster. Charge ∥ Auth0 OK gdy `session*` ≠ `rate*` / `charge*` / `extraction*`. FE ∥ Charge po Wave A, jeśli pliki rozłączne; **U-routes-breadth** i tak wymaga UI w plasterze BC.

---

## Skills

Obowiązkowe: `nowy-plaster`, `zamknij-plaster`, `lowca-duplikatow` (przed kodem), `migracja-rls`, `openfga-change` (gdy model FGA), `ekstraktor` (granica accept), `pr-review`, `knowledge-retrieve` ≤8 kart.

**Nie:** `module-factory` na 70 BC.

Po D0: pętla `docs/ops/post-plaster.md`. Nie edytuj AGENTS / `.cursorignore` poza D0.
