# Plan realizacji OmniRoute — jedyny kanon (oś pin 2026-09-08c)

**Jedna oś.** Pin **2026-09-08c** + Fala AI + Fala BR. Nic z pinu nie wypada.
**Teraz** = [CURRENT.md](state/CURRENT.md). **Oś** = ten plik. Historia fabryki
(mermaid 0–D, Wave A, Charge, rzeka T3→CI9) = [PLAN-HISTORIA.md](state/PLAN-HISTORIA.md).
Rdzeń: RLS, HITL, LLM nie liczy, Decimal, `charge` = marża, `source_ref`.

**Alias (nie kanon):** [PROGRAM-12M.md](state/PROGRAM-12M.md).  
**Plan Cursor (historia):** `.cursor/plans/omniroute-realizacja.plan.md` — nie czytaj z niego „następny”.  
**ADR:** [0001](adr/0001-cursor-software-factory-weryfikacja.md) · [0002](adr/0002-frontend-platform-2026.md) · [0003](adr/0003-frontend-ui-system-2026.md)  
**Repo:** https://github.com/Spawn2018/OmniRoute

<!-- os-status:start -->
**Następny:** **644.0** leftover EXP0.9 `limited_quantity` HITL na `dangerous_good` (zero live IMO / LLM klasy / grupy 1.xA). D9d PDF-QR / D9e skan / D9f pdf-zpl live / matching T5 / FK kontekstu / T8 live / D6b / D7b / fx×FV / auto-copy U1 / similar SQL / F2b / auto-resync salda / live 409 / live poll / Expo BR2.3 / warning-jako-fakt / N8 / T6 live / P5c / N6 auto charge = park `/noc`. **588.0** SH-R16-4 UXCL = park `/noc`.
<!-- os-status:end -->

Historia osi 0→Q1: [PLAN-HISTORIA.md](state/PLAN-HISTORIA.md).

---

## Jak czytać

| Plik | Rola |
|---|---|
| **ten dokument** | Jedyny plan: oś pinu, standing, gate, kolejka. |
| [VISION.md](VISION.md) | Czym jest produkt (A.1: dwie skóry + pomiar). |
| [CURRENT.md](state/CURRENT.md) | **Teraz** — ostatni plaster, następny, spec. |
| [PROGRESS.md](state/PROGRESS.md) | Historia plastrów — fakty, nie kolejka. |
| [MODULES.md](MODULES.md) | Żywy rejestr tego, co jest w kodzie. |
| [PLAN-HISTORIA.md](state/PLAN-HISTORIA.md) | Fabryka 0–D, Wave A, Charge, rzeka nocy. Nie „następny”. |
| Badania `D:\OMNIROUTE-badania` | Surowiec (plany, kanony, agenci, kontrakty). Promocja do repo **tylko** po stopie `/noc` + jawnym poleceniu. `12` = SUPERSEDED. |

Gdy CURRENT wskazuje wydmuszkę: najpierw **Plan** (`/plan-modul`), potem `/plaster`. Zakaz 70 pustych stubów. „Następny plaster” pisze tylko CURRENT (i `just docs` → `os-status`).

---

## Cel produktu

Z [VISION.md](VISION.md) **A.1** (dosłownie, nie „platforma spedycyjna”):

OmniRoute to wielotenantowe oprogramowanie klasy „inteligentne zarządzanie
firmą”, które obsługuje jednocześnie obie strony rynku transportu: wykonawcę
usługi (spedycja, przewoźnik, operator logistyczny) i jej zleceniodawcę
(korporacja, załadowca, właściciel łańcucha dostaw), a jego przewagą nie jest
lista funkcji, lecz to, że **każda podpowiedź systemu jest mierzona metodą
naukową i rozliczana z tego, ile realnie oszczędziła**.

Jedna baza, dwie skóry, nie dwa codebase’y. A.2–A.5 i C.3: ten sam plik wizji.
Horyzont „12m” = standing rules i anti-cele, nie „czekaj rok na moduły”.

## Cel jakości (4,4–5)

Spedytor kończy job w czasie, który da się zmierzyć. Następny człowiek czyta kod i dokument jak czyjąś utrzymywaną rzecz, nie jak noc generatora. Cokolwiek nie jest **4,4** zostaje nazwane albo spłacone w tej samej cegiełce. Zielony gate jest podłogą, nie celem.

Nota **4,4–5** stawia karta i diff — nie prompt „pisz jak senior”. Kalibracja: **5,0** = `charge.margin` + niemutowalna `rate_line` + `source_ref` + HITL przed stawką; **4,4** = to samo plus drobna kopia na trzy ruchy `/refaktor`; **3,x** = generator (bliźniaczy katalog, sklonowany nagłówek modelu); **2,x** = nowa nazwa M-xx, stara tabela. Cel 4,4–5 = **Grupa A** (własna tabela, zapis, izolacja). Tablice-odczyty Fal 3–11 nie idą na 5,0: makieta w docs albo prawdziwy moduł.

Trzy twarde reguły: (1) szybkość jest liczbą z budżetu AGENTS albo jawnym N/A — k6-echo nie zamyka; (2) dług ukryty zakazany — wiersz w [docs-debt.md](ops/docs-debt.md) z „dlaczego” albo gwoźdź w diffie; (3) komentarz mówi *dlaczego* (ustawa, HC), linia powtarzająca kod obniża notę. Dokumentacja programu ≠ `AGENTS.md`.

Procedura nie jedzie „aż 5,0 sama”. Hamulec: karta [post-plaster.md](ops/post-plaster.md). Spłata starego 3,x: `/refaktor` (max 3). Kolejka: **Fala E** (zamknięta), **Fala S** (pogłębienia; live Auth0/portale/M-02 konsument gdy CURRENT wskaże to Q), potem **P0** + oś pinu **2026-09-08c** (O/I/U/T/D/P/G2/F/C/V/W/X/WA/Plat/Demo/CT/CI/G/EXP/K0), potem **Fala AI** (silniki nad HITL) i **Fala BR** (moduły brakujące; start HHL: BR3.0 / BR6.0 / BR2.0). Leftover HITL/SQL **nie** jest skipem nocy. F9.1 bez żywej nazwy aż wiersze **S56–S58** (zamknięte). Nie zgaduj 71–212. Puste ID zostają puste.

---

## Standing rules (zawsze, też po powrocie do MODULES)

1. `organization_id` w każdej tabeli biznesowej + RLS + test izolacji. Runtime: rola `omniroute_app` **NOBYPASSRLS** (nie superuser).
2. Auth produkcyjny **gdy będzie tenant** = Auth0 BFF + cookie httpOnly (Code + PKCE). **I1/I2 nie teraz.** Sesja dziś = email+hasło+JWT (0.12 + 0.15). Hello HS256 = local/CI. 0.12/0.15 **nie** są IdP.
3. Sekrety: **GitHub Encrypted Secrets** + `.env` w gitignore. **Zakaz Infisical.** JWT/AUTH0 nie w YAML.
4. GitHub **Pro później**. Branch protection = procedura + hooki, nie required check UI na Free (403).
5. Kwoty: **Decimal / Numeric**, komponent `<Money/>`. LLM **nie liczy**.
6. **charge** = jedyna prawda o marży (kupno+sprzedaż na jednym rekordzie). **rate_line** niemutowalna + `source_ref`.
7. Accept HITL → `rate_line` przez **orchestrację API** (ten sam request/transakcja). `ExtractionService` **nie** importuje rates.
8. PDF HITL w zakresie = **U-pdf-spans** (viewer + spany, lazy pdf.js). Nie teatr OCR.
9. Paleta ⌘K = akcje operatora = **U-palette-ops**, nie sam skok po trasach.
10. Ewaluacje AI = **syntetyki**. Zero PDF klienta w git.
11. Temporal / Hatchet / outbox **zakazane**, dopóki nie ma realnego zdarzenia async **między** BC poza HTTP.
12. `Informacje z claude/` zostaje na dysku. Nie dumpuj do nowych docs.
13. Echo recipe ≠ DoD. `can_*` ≠ `member`. Recenzent ≠ każdy member.
14. **Zakaz 70 pustych stubów** / `module-factory` na cały rejestr.
15. Każdy endpoint: jawne uprawnienie OpenFGA. Brak = deny.
16. **Exit Wave FE** = **wszystkie** ID `U-*`. Adapter+RTL **nie** zamyka fali. Twierdzenie „scaffold 2026 + powierzchnia 2026” **zakazane**, dopóki każdy U-* nie ma widocznego DoD i gate, który pada.

### AI Act (produkt, nie PDF prawny)

Ekstrakcja HITL, brak scoringu osoby fizycznej = **minimal risk**. **Zakaz:** automatyczny credit scoring `natural_person` / JDG. Art. 50 = label w UI (**U-art50**), nie notatka prawna. D0 **nie** zdejmuje HITL / „LLM nigdy nie liczy”.

---

## Gate dziś vs cel DoD (uczciwość)

Źródło: audyt 2026-08-31 + stan 2026-09-01. **Nie zamykaj plastra ani nie twierdź „pełny DoD”, jeśli recipe to `echo`.**

**Podział bramki (audyt runów #79–#88):** `gate` = `code-gate` + `meta-gate`. CI woła je jako **dwa niezależne joby** (`gate` i `meta`), nie `just gate`. Powód: meta-checki stały przed kodem w łańcuchu fail-fast i przez siedem pushy zasłoniły ruff, mypy, testy i import-linter — w tym oknie przeszedł niezauważony realny błąd granic modułów. Żadna kategoria nie może już tłumić drugiej.

| Obietnica | Egzekwowane teraz | Kiedy |
|---|---|---|
| ruff + mypy | tak `just check` | — |
| pytest unit + integration | tak CI | — |
| import-linter | tak `just arch` | — |
| frontend typecheck | tak `frontend-typecheck` w `code-gate` | — |
| vitest | tak `frontend-test` w `code-gate` | — |
| playwright + axe | tak `frontend-e2e` w `code-gate` | Chromium; nie Firefox |
| cov ≥ 80% | tak `test-unit --cov-fail-under=80` | — |
| jscpd ≤ 3% | tak `just dup` w `code-gate` | — |
| openapi-ts | tak `just api-types` + `frontend/src/api/` | regeneruj przy zmianie API |
| size-limit / perf | tak `just perf` initial JS gzip < 250 kB | **k6 p95 nadal stub/echo** |
| agentlint | tak `just agentlint` + baseline, job `meta` | podpis pod kontraktem: zmiana `AGENTS.md` / `.cursor/rules` wymaga `agentlint.py --write` **w tym samym commicie** |
| styl slopu (OS-4) | tak `just craft-style` + sufit w `quality-floor`, job `meta` | TODO, `except Exception`, echo-komentarz, `float()`, `as any`; funkcje >40 linii tylko w dół. **Nie** smak ani merytoryka. |
| just docs (status OS) | tak `just docs-check`, job `meta` | CURRENT → README / ARCHITECTURE / PLAN |
| bramka przed push | hook `pre-push` = pełne `just gate` (~70 s) | **lokalnie, per-clone.** Wymaga `just hooks` po każdym clone; CI tego nie widzi. `--no-verify` omija. Migracje, `audit`, promptfoo, integration nadal tylko w CI. Sam składa PATH; błąd agentlinta wraca po ~96 s — szybciej `just meta-gate` (~1 s) |

**Nie cofaj hotfixów CI:** `005` `current_database()` zamiast `Connection.url`; agent-refs URI ≠ plik; agentlint baseline; conftest — osobne `DO $$`; live HTTP = `httpx` AsyncClient; `rate_line` mutate = commit + select kolumny.

---

Historia Fabryki 0–D, Wave A (D0–0.23) i Charge 0.24–1.3: [PLAN-HISTORIA.md](state/PLAN-HISTORIA.md). ID zostają tam; tu nie sterują nocą.

## Wave FE U-* — ID na origin; Exit **nie** claim

U0 adapter / U1 shell / U2 tabela ADR weszły jako 0.5 / 0.6 / openapi-ts — to **scaffold**, nie Exit Wave FE.

| ID | Operator zobaczy | Gate co padnie | Status |
|---|---|---|---|
| **U-density** | compact + toggle na listach biznesowych | lista bez compact / bez toggle | ID na origin |
| **U-palette-ops** | ⌘K: extract, accept-focus, save-view, clear-session | paleta tylko nawigacja | ID na origin |
| **U-pdf-spans** | PDF + highlight spanów HITL, lazy pdf.js | brak highlightów; PDF w initial JS; gzip > 250 kB | ID na origin |
| **U-routes-breadth** | każdy BC z jobem operatora = trasa w tym samym plasterze | backend-only charge/rate_line/session | **standing**, nie 70 UI |
| **U-a11y** | skip-to-main, focus-visible, Tab/⌘K | tylko mysz; zamknięcie na RTL | ID na origin |
| **U-size-limit-real** | `just perf` failuje CI przy ≥ 250 kB | recipe-echo | ID na origin |
| **U-art50** | label „propozycja AI” na szkicu HITL | draft bez labelu | ID na origin |
| **U-admin-ref** | gęsty sidebar/toolbar/⌘K; pulpit = joby | „adapter = Exit Wave FE” | ID na origin |

**Zakaz claim:** „scaffold 2026 + powierzchnia 2026”, „70 UI”, zamykanie fali na adapter+RTL. U-routes-breadth = standing na **kolejne** BC, nie dowód że powierzchnia 2026 jest skończona.

### Wave FE — leftover po audycie UI (2026-09-01) — **nie Q1**

ADR-0003 + makiety [docs/design/](design/README.md). **Nie** konsumują slotu Q1 (M-05). Każdy ID = osobny plaster **po** Planie tej pozycji albo wpleciony w najbliższy plaster UI, który i tak rusza dany plik. Zero kodu `frontend/` przy samym ADR.

| ID | Operator zobaczy | Gate co padnie | Zależność |
|---|---|---|---|
| **U-oklch-dark** | tokeny OKLCH, motyw jasny/ciemny, kontrast AA | hex-only; brak `.dark`; para tokenów < 4.5:1 | `index.css` · 51.0 zamknięty |
| **U-money-align** | kwota wyrównana do przecinka + kod waluty | `<Money/>` bez osi dziesiętnej | `money.tsx` · 52.0 zamknięty |
| **U-condensed** | trzeci tryb gęstości na gridzie stawek | condensed globalnie albo brak na `rate_line` | DataTableShell · 53.0 zamknięty |
| **U-primitives-json** | `frontend/components.json` base radix | `shadcn add` bez `-b radix` wciąga Base UI | CLI · 54.0 zamknięty |
| **U-i18n-structure** | klucze + locale format; jeden język (pl) w paczce | hardcoded string w **nowym** ekranie | nowe trasy · 55.0 zamknięty |
| **U-playwright-axe** | 3 ścieżki E2E + axe na trasie | brak Playwright w gate; axe poza CI | po U-oklch-dark · 56.0 zamknięty |
| **U-print** | arkusz druku B/L / FV / list | `@media print` chaos albo PDF-teatr | Fala 5/6 · 57.0 zamknięty |
| **U-omniroute-ui-dna** | rail `--ink` / `--on-ink` z `#v-quote` / `#v-ship` | druga paleta albo brak nazwy `--ink` | `index.css` · 127.0 zamknięty |

**Wizja (canvas 06) — parked aż będą dane:**

| Ekran | Najwcześniej |
|---|---|
| Watchtower (mapa + wyjątki) | po M-05 **i** M-35–M-37; mapa = lazy chunk, nie initial 250 kB |
| Oś multimodalna | Fala 5 (tracking) |
| Portale klienta / przewoźnika | Fala 10 (M-61+) |

Optimistic UI: wolno na filtrach/widokach/kolumnach. **Zakaz** na kwocie, `charge`, `rate_line`, accept HITL.

---

## Auth0 — odroczone

I1 (BFF + PKCE + cookie; org z `app_metadata`; first-login bez org = odmowa) i I2 (RS256 JWKS; hello OFF staging/prod) **nie teraz** — brak tenanta. Nie pytać. Hasła + refresh zostają sesją. **270.0** = HITL katalog `idp_connector` (token `auth0`, fixture); to **nie** jest login i **nie** zastępuje 0.12/0.15. Zero live HTTP / JWKS / BFF / „hello OAuth”. Organizations feature **nie** w I1. OpenFGA = SoT ról (first-login = member; reviewer ręczny seed).

Gdy user **ma** tenant: SPA Vite → BFF FastAPI → Auth0; cookie HttpOnly; Secure; SameSite=Lax; region EU / SCC jeśli plan pozwala. **Nie** w tym samym plasterze co hasła.

**Park — live public / Cloudflare (2026-09-13):** właściciel chce Cloudflare jako warstwę bezpieczeństwa **zanim** SPA jest publiczna. To **nie** jest Q `/noc` i **nie** zdejmuje leftover **S53** Auth0 I1/I2. Access (Zero Trust przed hostem) ≠ IdP tenanta. Pin **2026-09-08c** bez zmian.
[WYCOFANE 2026-09-13: „431.0 zostaje następnym plastrem” — **431.0** jest w kodzie;
żywe „następny” = tylko CURRENT / `os-status`]. Kanon: [VISION.md](VISION.md) § B.8.
Karta STRIDE: [threat-model-tenant-hitl.md](ops/threat-model-tenant-hitl.md) (dopisek edge).

---

## Moduły w kodzie (żywy rejestr)

Szczegół: [MODULES.md](MODULES.md). Poniżej odpowiedzialność, zysk, plastry, anti-confusion.

### M-01 tenancy — fundament

**Za co:** izolacja tenantów, tożsamość sesji, OpenFGA.  
**Daje:** RLS + test izolacji; JWT Bearer; hasła argon2id + refresh; `hello_token` off poza local/CI.  
**Plusy:** baza egzekwuje tenancy (NOBYPASSRLS); headery nie spoofują org; recenzent ≠ member.  
**Plastry:** 0.3, 0.4, 0.12, 0.15, 0.16 T1, 0.17 T2, 0.21 T4, 0.22 T5.  
**Nie:** IdP. 0.12/0.15 ≠ Auth0. Auth0 I1/I2 odroczone.

### M-02 outbox — fundament (79.0)

**Za co:** zdarzenia async **między** bounded contextami + idempotencja zapisu.  
**Daje:** `outbox_event` + `/outbox`; kind `inbound_message_saved` po zapisie wiadomości.  
**Nie:** Temporal / Hatchet / worker / konsument. Nie mylić z 0.4 (OpenFGA).

### M-03 organization_setting — fundament (3.0)

**Za co:** konfiguracja jako dane (HC-02). Allowlista `default_currency`.  
**Daje:** `/organization-settings`; RLS; waluta tenanta w bazie, nie w env.  
**Plusy:** zmiana konfiguracji bez deployu; nie sekrety.  
**Nie:** Infisical, `table_view`, sekrety tenanta, env jako źródło prawdy.

### M-06 charge_code — fundament (1.0)

**Za co:** słownik kodów opłat + aliasy.  
**Daje:** `/charge-codes`; brak luźnego stringa w stawkach.  
**Nie:** `rate_line`, `charge`, marża.

### M-07 rate_line — fundament (1.1)

**Za co:** niemutowalna stawka kupna + `source_ref`.  
**Daje:** `/rate-lines`; zmiana = nowy wiersz + `superseded_by`.  
**Plusy:** audyt pochodzenia; LLM nie wstawia stawki bez HITL (1.3).  
**Nie:** marża; `charge`; k6 na 50k.

### M-08 charge — fundament (1.2)

**Za co:** jedyna prawda o marży — kupno i sprzedaż na jednym rekordzie.  
**Daje:** `margin()` w kodzie; `/charges`.  
**Nie:** accept HITL; liczenie marży w quotation / LLM.

### M-20 extraction HITL — fundament

**Za co:** wyciąg z dokumentu → draft → człowiek accept/reject.  
**Daje:** kolejka HITL, instructor+guard, docling A/B, live HTTP PG (0.18), accept→`rate_line` (1.3), label Art. 50, PDF+spany, Presidio stub + 10 `synth://`.  
**Plusy:** nic z ekstrakcji nie idzie do stawek bez HITL; `ExtractionService` nie importuje rates.  
**Plastry:** 0.7–0.14, T0, 0.18, 1.3, U-art50, U-pdf-spans, 2.1–2.2.  
**Nie:** OCR-teatr; Presidio-all; żywy OpenAI w gate; 30 PDF klienta; import rates.

### M-21 quotation — fundament (2.0)

**Za co:** wycena SQL z **bieżącego** `rate_line` (`INSERT…SELECT`).  
**Daje:** `/quotations`; RLS.  
**Plusy:** Postgres liczy z indeksem; nie Python na 50k.  
**Nie:** k6 p95 na pustej tabeli; marża (zostaje w `charge`).

---

## Dwa tryby pracy (jak Agent / Plan / Multitask)

Kolejka poniżej **zdejmuje z Ciebie pamiętanie „co dalej”**. Agent czyta `CURRENT.md` + tę sekcję. Nie zgaduje.

| Tryb w Cursorze | Kiedy | Komenda | Co wolno |
|---|---|---|---|
| **Plan** | Każda nowa pozycja kolejki, zanim powstanie kod — zwłaszcza **wydmuszka** (moduł z katalogu M-xx, którego jeszcze nie ma w `MODULES.md` jako fundament) | `/plan-modul` | Rozmowa: job operatora, tabele, UI, poza zakresem, kolizje ID. Wynik: delta w `docs/deltas/open/` + spec szkielet + `CURRENT.md` z zakresem. **Zero kodu produktu.** |
| **Agent** | Dopiero gdy Plan tej pozycji jest **zaakceptowany** (delta bez „DO USTALENIA” blokujących) | `/plaster` | Pionowy plaster: migracja → RLS → izolacja → API → UI → test → post-plaster → push. |
| **Refaktor** | `CURRENT.md` **Etap: Refaktor** (Fala E, Q-E1 i kolejne sloty `/refaktor`) | `/refaktor` | Max 3 ruchy, zachowanie bez zmian, testy bez zmiany asercji. Nie nowy M-xx. |

`/plaster` przy `CURRENT.md` **Etap: Plan** = **stop**. Nie implementuj. Powiedz, żeby przełączyć na Plan i odpalić `/plan-modul`.
`/plaster` przy **Etap: Refaktor** = **stop**. Odpal `/refaktor`.

Wydmuszka ≠ 70 pustych stubów w repo. Plan ustala **jeden** plaster. Kod powstaje dopiero w Agent.

---

## Kolejka realizacji (jedno po drugim)

Semantyka kolumn (Fala *): `ID | Co | Status | Leftover | Źródło | Zakaz`.
Status tylko: `DONE` / `HITL` / `leftover silnik` / `park live` / `czeka`.
Tabele historyczne S/Q zachowują swoje kolumny — ID nie ginie. Dump CT/TMS =
jedno zdanie + link do badań `03` / `04b`. Nowy leftover = dopisek w Uwagach
istniejącego wiersza.

Źródło nazw: archiwum `REJESTR-MODULOW-I-PLAN-v2.md` (na dysku, nie dumpować specyfikacji). **Kolejność budowy ≠ numer M-xx** — numery archiwum i żywy kod się rozjechały (patrz mapa kolizji).

Po zamknięciu plastra `CURRENT.md` = **następna pozycja Q**. Nie pytaj operatora „co chcesz”. Wykonaj tryb z kolumny. Q1 ma trzy żywe plastry (4.0 → 4.1 → 4.2); Q2 dopiero po 4.2.

Po Fali 11 i leftover FE: **Fala E (Q-E1…E4)**, potem **Fala S** (S1…). Nie F9.1 po Q-E4. Q-E0 = 59.0 (kanon jakości). F9.1 = S56–S58.

### Mapa kolizji ID (czytaj zanim nazwiesz tabelę)

| Archiwum | Żywy kod dziś | Skutek |
|---|---|---|
| M-06 słownik opłat | **M-06** `charge_code` | fundament; aliasy na wierszu, bez pgvector |
| M-07 waluty i czas | **kolizja** — żywe **M-07** = `rate_line` | Q5 żywy ID **M-23** `nbp_rate` |
| M-08 towary niebezpieczne | **kolizja** — żywe **M-08** = `charge` | Q6 żywy ID **M-52** `dangerous_good` |
| M-17 stawki statyczne | pokryte przez żywe **M-07** `rate_line` | nie startuj drugiego silnika stawek |
| M-22 narzuty i marża | pokryte przez żywe **M-08** `charge` | marża zostaje w `margin()` |
| M-52 ślad węglowy (katalog) | żywe **M-52** = `dangerous_good` | ślad = nowy żywy ID przy CBAM (Fala S faza 10); nie nadpisuj DG |
| M-57 serwer MCP (katalog) | żywe **M-57** = tablica extract | MCP później; nie nadpisuj. Kat. M-58 = pogłębienie M-57 (**S56**) |
| Historyczne **F11.0** M-68 | Fala F **F11** książka PP | kropka = obserwowalność (48.0); F11 bez kropki = Poczta Polska |
| Historyczne **F9.0** M-57 | Fala F **F9** adapter ERP | F9.1 = S56–S58 (zamknięte); F9 = FS+FZ do FK |
| Fala **O** biurko ocean | M-51 `ocean_lcl` | O = wycena/kupno (M-19/M-30/M-31); LCL = odcinek zlecenia |
| Arch. M-179 szyna decyzji | **kolizja M-57** | S11 żywy ID **M-71** `operator_decision` |
| Arch. M-91 zbiorcze FV | brak kolizji z żywym M-40 | S43 żywy ID **M-91** `collective_invoice`; nie nadpisuj `sales_invoice` |
| M-35 vs arch. M-89 booking | default: **jedna** tabela `shipment` | dwa obiekty tylko gdy Plan **S28** udowodni dwa joby |

### Fala 0 — już w kodzie (nie wracaj)

M-01 tenancy · M-03 `organization_setting` (część: `default_currency`) · M-06 `charge_code` · M-07 `rate_line` · M-08 `charge` · M-09 `commodity_code` · M-20 ekstrakcja HITL · M-21 `quotation` · M-23 `nbp_rate`. OpenFGA hello = kawałek archiwum M-04, **nie** IdP.

### Fala 1 — zamknięta (fundament; pogłębienia = Fala S)

| Q | Co | Tryb startu | Status |
|---|---|---|---|
| Q1.0 | M-05 plaster **4.0** `port` + seed `improved-un-locodes` + `resolve` + `/ports` | Plaster (delta `docs/deltas/archived/4.0-port.md`) | zamknięty |
| Q1.1 | M-05 plaster **4.1** `location` + `location_zone_member` | Plaster (delta `docs/deltas/archived/4.1-location-zones.md`) | zamknięty |
| Q1.2 | M-05 plaster **4.2** `terminal` + World Port Index | Plaster (delta `docs/deltas/archived/4.2-terminal-wpi.md`) | zamknięty |
| **Q2** | Archiwum **M-10 Kontrahenci** | Plan → plaster | zamknięty (`docs/deltas/archived/5.0-party.md`) |
| Q3 | Pogłębienie żywego **M-21** `quotation` o port + kontrahent (lista/filtry; SQL na istniejących `rate_line`; nie marża; nie k6) | Plan → plaster | zamknięty (`docs/deltas/archived/5.1-quotation-port-party.md`) |
| Q4 | Archiwum **M-09 Kody towarowe** | Plan → plaster | zamknięty (`docs/deltas/archived/5.2-commodity-code.md`) |
| Q5 | **Waluty i kurs NBP** (archiwum M-07; **nie** nadpisuj żywego M-07) | Plan → plaster | zamknięty (`docs/deltas/archived/6.0-nbp-rate.md`) |
| Q6 | **Towary niebezpieczne** (archiwum M-08; **nie** nadpisuj żywego M-08) | Plan → plaster | zamknięty (`docs/deltas/archived/7.0-dangerous-good.md`) |
| F2.0 | **M-11 Automatyczne kontakty** | Plan → plaster | zamknięty (`docs/deltas/archived/8.0-party-email-match.md`) |
| F2.1 | **M-12 Sieci i stowarzyszenia** | Plan → plaster | zamknięty (`docs/deltas/archived/9.0-network.md`) |
| F2.2 | **M-13 Karta wyników kontrahenta** | Plan → plaster | zamknięty (`docs/deltas/archived/10.0-party-scorecard.md`) |
| F2.3 | **M-16 Procedury operacyjne klienta** | Plan → plaster | zamknięty (`docs/deltas/archived/11.0-customer-sop.md`) |
| F2.4 | **M-18 Opłaty portowe warunkowe** | Plan → plaster | zamknięty (`docs/deltas/archived/12.0-port-surcharge.md`) |
| F2.5 | **M-19 Stawki live i kanały** | Plan → plaster | zamknięty (`docs/deltas/archived/13.0-channel-quote.md`) |
| F2.6 | **M-14 Ocena kredytowa** | Plan → plaster | zamknięty (`docs/deltas/archived/14.0-credit-review.md`) |
| F2.7 | **M-15 Wirtualny Dyrektor Finansowy** | Plan → plaster | zamknięty (`docs/deltas/archived/15.0-finance-board.md`) |
| F3.0 | **M-23 Waluty w ofercie** | 16.0 | zamknięty (`docs/deltas/archived/16.0-quotation-nbp.md`) |
| F3.1 | **M-24 Ryzyko oferty** | 17.0 | zamknięty (`docs/deltas/archived/17.0-offer-risk.md`) |
| F3.2 | **M-25 Negocjacja i wynik** | 18.0 | zamknięty (`docs/deltas/archived/18.0-offer-negotiation.md`) |
| F3.3 | **M-26 Dokument oferty** | 19.0 | zamknięty (`docs/deltas/archived/19.0-offer-document.md`) |
| F3.4 | **M-27 Wycena wsadowa** | 20.0 | zamknięty (`docs/deltas/archived/20.0-quotation-batch.md`) |
| F3.5 | **M-28 Zapytania od klientów** | 21.0 | zamknięty (`docs/deltas/archived/21.0-customer-inquiry.md`) |
| F3.6 | **M-29 Wykrywanie akceptacji** | 22.0 | zamknięty (`docs/deltas/archived/22.0-offer-acceptance.md`) |
| F3.7 | **M-30 Zapytania do agentów/armatorów** | 23.0 | zamknięty (`docs/deltas/archived/23.0-carrier-inquiry.md`) |
| F3.8 | **M-31 Porównanie odpowiedzi** | 24.0 | zamknięty (`docs/deltas/archived/24.0-response-comparison.md`) |
| F4.0 | **M-32 Integracja pocztowa** | 25.0 | zamknięty (`docs/deltas/archived/25.0-mail-integration.md`) |
| F4.1 | **M-33 Dodatek do Outlooka** | 26.0 | zamknięty (`docs/deltas/archived/26.0-mail-client.md`) |
| F4.2 | **M-34 Powiadomienia** | 27.0 | zamknięty (`docs/deltas/archived/27.0-operator-notice.md`) |
| F5.0 | **M-35 Zlecenie** | 28.0 | zamknięty (`docs/deltas/archived/28.0-shipment.md`) |
| F5.1 | **M-36 Tracking** | 29.0 | zamknięty (`docs/deltas/archived/29.0-tracking.md`) |
| F5.2 | **M-37 Wyjątki** | 30.0 | zamknięty (`docs/deltas/archived/30.0-operational-exception.md`) |
| F5.3 | **M-38 Dokumenty zlecenia** | 31.0 | zamknięty (`docs/deltas/archived/31.0-shipment-document.md`) |
| F5.4 | **M-39 EDI** | 32.0 | zamknięty (`docs/deltas/archived/32.0-edi-message.md`) |
| F6.0 | **M-40 Fakturowanie i KSeF** | 33.0 | zamknięty (`docs/deltas/archived/33.0-sales-invoice.md`) |
| F6.1 | **M-41 Rozliczenie wyceny z fakturą** | 34.0 | zamknięty (`docs/deltas/archived/34.0-quote-invoice-settlement.md`) |
| F6.2 | **M-42 Bank i płatności** | 35.0 | zamknięty (`docs/deltas/archived/35.0-bank-payment.md`) |
| F6.3 | **M-43 Koszt pieniądza** | 36.0 | zamknięty (`docs/deltas/archived/36.0-money-cost.md`) |
| F6.4 | **M-44 Różnice kursowe** | 37.0 | zamknięty (`docs/deltas/archived/37.0-fx-difference.md`) |
| F6.5 | **M-45 Przepływy** | 38.0 | zamknięty (`docs/deltas/archived/38.0-cash-flow.md`) |
| F6.6 | **M-46 Koszt obsługi klienta** | 39.0 | zamknięty (`docs/deltas/archived/39.0-cost-to-serve.md`) |
| F6.7 | **M-47 Księgowość (integracja)** | 40.0 | zamknięty (`docs/deltas/archived/40.0-bookkeeping.md`) |
| F7.0 | **M-48 Transport drogowy** | 41.0 | zamknięty (`docs/deltas/archived/41.0-road-transport.md`) |
| F7.1 | **M-49 Kolej intermodalna** | 42.0 | zamknięty (`docs/deltas/archived/42.0-intermodal-rail.md`) |
| F7.2 | **M-50 Kolej z Chin** | 43.0 | zamknięty (`docs/deltas/archived/43.0-china-rail.md`) |
| F7.3 | **M-51 Drobnica morska** | 44.0 | zamknięty (`docs/deltas/archived/44.0-ocean-lcl.md`) |
| F8.0 | **M-53 Sankcje** | 45.0 | zamknięty (`docs/deltas/archived/45.0-sanctions.md`) |
| F8.1 | **M-56 RODO** | 46.0 | zamknięty (`docs/deltas/archived/46.0-gdpr.md`) |
| F9.0 | **M-57** | 47.0 | zamknięty (`docs/deltas/archived/47.0-ai-copilot.md`) |
| F9.1 | **M-58–M-60** | — | bez żywej nazwy aż **S56–S58**; nie zgaduj po Q-E |
| F10 | **M-61–M-67** | parked | odblokowanie **S55** (po Auth0 **S53**) |
| F11.0 | **M-68 Obserwowalność** | 48.0 | zamknięty (`docs/deltas/archived/48.0-observability.md`) |
| F11.1 | **M-69 Jakość** | 49.0 | zamknięty (`docs/deltas/archived/49.0-extraction-quality.md`) |
| F11.2 | **M-70 Wdrożenie** | 50.0 | zamknięty (`docs/deltas/archived/50.0-tenant-rollout.md`) |
| **Q-E0** | Kanon jakości 4,4–5 w tym dokumencie | 59.0 | zamknięty (ten wiersz) |
| **Q-E1** | `/refaktor` — katalogi Grupa A do 4,4 (`catalog-parts`) | 60.0 | zamknięty (`docs/deltas/archived/60.0-catalog-parts.md`) |
| **Q-E2** | Testy przez Alembic; pomiar wyceny (EXPLAIN / p95 albo N/A z liczbą wierszy) | 61.0 | zamknięty (`docs/deltas/archived/61.0-alembic-quote-budget.md`) |
| **Q-E3** | How-to jobów zapisu + C4 w ARCHITECTURE | 62.0 | zamknięty (`docs/deltas/archived/62.0-operator-howto-c4.md`) |
| **Q-E4** | Threat model tenant+HITL + CodeQL w CI | 63.0 | zamknięty (`docs/deltas/archived/63.0-threat-model-codeql.md`) |
| po Q-E4 | **Fala S**, named parks (Auth0 / portale / AIS) | — | w osi; live gdy CURRENT wskaże Q |
| po parks | **P0** → pełna oś pinu **2026-09-08c** (O/I/U/T/D/P/G2/F/C/V/W/X/Plat/CT/CI/G/EXP) | Plan → plaster | O4 138.0 zamknięty. [WYCOFANE 2026-09-13: „O5 139.0 następny” — żywe „następny” = tylko CURRENT / `os-status`] |

### Fala S — pogłębienie wydmuszek (po Q-E4, nie zamiast Q-E1)

To **nie** jest nowy produkt. Fale 0–11 zostają fundamentem. Każdy wiersz S zdejmuje **jedno** „nie X” z [MODULES.md](MODULES.md) (obiekt → silnik → karta wieży). `/plan-modul` potem `/plaster`. WIP=1. LLM nie liczy. HITL zostaje.

**Nie startuj S1 przy Fali E.** CURRENT przy Q-E2…E4 = kolejka E (Plan albo `/refaktor`), nie S1. Po zamknięciu Q-E4: `CURRENT` = **S1**, Etap **Plan**.

Reguły kolejności (żeby `/noc` nie złożył awarii):

1. Tabela + RLS zanim HTTP.
2. Szyna Akceptuj/Zmień (**S11**, nowy żywy ID — **nie** M-57) i SOP zanim wysyłka.
3. Ingest Graph (**S15**) ≠ send (**S18**). IMAP = **S17**, nie w tym samym plasterze co Graph.
4. Screening i kredyt (**S25–S27**) zanim `shipment` (**S28**).
5. Auth0 (**S53**) zanim portale (**S55**).
6. Katalog 71–212 **wpinany** gdy jest poprzednik (faza 10), nie odliczany od 71.
7. COVERED: nie drugi silnik pod arch. M-17 / M-22.
8. Po pinie 2026-09-08 `/noc` jedzie leftover HITL/SQL z CURRENT. Named park **live** (S53/S55/konsument M-02) tylko gdy CURRENT wskaże to Q — nie zgaduj S53 przy cutoffie T3.

| S | Co | Tryb | Status | Powód / poza zakresem tego wiersza |
|---|---|---|---|---|
| **S1** | Żywe **M-32** tabela wiadomości + draft, fixture | 64.0 | zamknięty (`docs/deltas/archived/64.0-inbound-message.md`) |
| S2 | Żywe **M-11** `resolve_email` na wiadomości | 65.0 | zamknięty (`docs/deltas/archived/65.0-inbound-resolve-email.md`) |
| S3 | Żywe **M-20** treść/załącznik maila → extract | 66.0 | zamknięty (`docs/deltas/archived/66.0-inbound-extract.md`) | HITL zostaje. Serwis nie zapisuje `rate_line`. S3 = treść, nie blob |
| S4 | Żywe **M-28** obiekt RFQ powiązany z wiadomością | 67.0 | zamknięty (`docs/deltas/archived/67.0-customer-rfq.md`) | Nie ślad wycen. S5 = silnik |
| S5 | Żywe **M-21** istniejący silnik na tym RFQ | 68.0 | zamknięty (`docs/deltas/archived/68.0-quotation-on-rfq.md`) | Nie nowy silnik. LLM nie liczy |
| S6 | Żywe **M-18** ewaluacja `applies_when` w SQL | 69.0 | zamknięty (`docs/deltas/archived/69.0-port-surcharge-when.md`) | Nie zapis marży do `charge` |
| S7 | Żywe **M-09** HS/CN na RFQ/wycenie | 70.0 | zamknięty (`docs/deltas/archived/70.0-hs-cn-on-rfq.md`) | Katalog jest. S7b: UN→M-52 |
| **S7b** | Leftover **UN z M-52** na RFQ/wycenie | 122.0 | zamknięty (`docs/deltas/archived/122.0-un-on-rfq.md`) | Etykieta ładunku. Nie LLM. Nie filtr stawki |
| S8 | Żywe **M-03** reszta + arch. M-84 (scalać) | 71.0 | zamknięty (`docs/deltas/archived/71.0-org-number-template.md`) | Prefiks i token szablonu. Nie licznik. Nie PDF |
| S9 | Żywe **M-26** dokument oferty | 72.0 | zamknięty (`docs/deltas/archived/72.0-offer-document-number.md`) | Numer na ofercie + print 57.0. Nie send |
| S10 | Żywe **M-16** SOP „kiedy nie wolno auto” | 73.0 | zamknięty (`docs/deltas/archived/73.0-sop-blocks-auto.md`) | `blocks_auto`. Nie send |
| **S11** | Arch. **M-179** szyna Akceptuj/Zmień/Odrzuć | 74.0 | zamknięty (`docs/deltas/archived/74.0-operator-decision.md`) | Żywy **M-71**. Nie M-57. `changed` = 121.0 |
| **S11b** | Leftover **`changed`** na `operator_decision` | 121.0 | zamknięty (`docs/deltas/archived/121.0-decision-changed.md`) | Trzeci werdykt + lock. Nie extract. Nie send |
| S12 | Żywe **M-34** tabela powiadomień | 75.0 | zamknięty (`docs/deltas/archived/75.0-operator-notice-table.md`) | Tabela. Filtr 27.0 = 123.0. Nie send |
| **S12b** | Leftover **filtr 27.0** na tablicy pending | 123.0 | zamknięty (`docs/deltas/archived/123.0-notice-pending-filter.md`) | Filtr kind. Nie auto-INSERT. Nie send |
| S13 | Żywe **M-57** draft maila obok extract | 76.0 | zamknięty (`docs/deltas/archived/76.0-mail-draft.md`) | Tabela. Accept przez S11. Nie send |
| S14 | Arch. **M-187** lock optymistyczny na decyzji | 77.0 | zamknięty (`docs/deltas/archived/77.0-decision-lock.md`) | `lock_version`. Nie nowa tabela |
| **S15** | Żywe **M-32** tylko ingest Graph | 78.0 | zamknięty (`docs/deltas/archived/78.0-graph-ingest.md`) | `graph://` + `external_id`. Live HTTP leftover. Nie send |
| **S16** | Żywe **M-02** outbox | 79.0 | zamknięty (`docs/deltas/archived/79.0-outbox.md`) | `inbound_message_saved`. Konsument leftover. Nie Temporal |
| S17 | Żywe **M-32** ingest IMAP / EmailEngine | 80.0 | zamknięty (`docs/deltas/archived/80.0-imap-ingest.md`) | `imap://` + `external_id`. Live leftover. Nie send |
| **S18** | Żywe **M-33** wysyłka po S11+S10 | 81.0 | zamknięty (`docs/deltas/archived/81.0-mail-send.md`) | Świadomy `mailto:` po accept. Graph HTTP leftover. Auto-send zakazane |
| S19 | Żywe **M-12** `network_member` | 82.0 | zamknięty (`docs/deltas/archived/82.0-network-member.md`) | Ręczny katalog. Portal leftover |
| S20 | Żywe **M-30** zapytanie do agenta | 83.0 | zamknięty (`docs/deltas/archived/83.0-carrier-inquiry.md`) | Buy side. Tabela. Live leftover |
| S21 | Żywe **M-19** live HTTP kanału **przy umowie** | parked | brak umowy (`docs/deltas/archived/S21-channel-http-parked.md`) | Nie teatr HTTP |
| S22 | Żywe **M-31** porównanie | 84.0 | zamknięty (`docs/deltas/archived/84.0-response-comparison-charge.md`) | Spread w `charge` / `margin()` |
| S23 | Żywe **M-25** wynik negocjacji | 85.0 | zamknięty (`docs/deltas/archived/85.0-offer-negotiation-result.md`) | Wskazanie kanału. Nie zamiast `margin()` |
| S24 | Żywe **M-29** won/lost; accept oferty przez S11 | 86.0 | zamknięty (`docs/deltas/archived/86.0-offer-acceptance-decision.md`) | Decyzja S11 na `quotation`. Nie accept extractu |
| S25 | Żywe **M-24** fakty ryzyka | 87.0 | zamknięty (`docs/deltas/archived/87.0-offer-risk-fact.md`) | Wskazanie recenzji. Nie scoring osoby |
| S26 | Żywe **M-14** recenzja + załącznik wywiadowni | 88.0 | zamknięty (`docs/deltas/archived/88.0-credit-review-bureau.md`) | Nie auto-limit |
| **S27** | Żywe **M-53** sankcje HTTP na `party` | 89.0 | zamknięty (`docs/deltas/archived/89.0-party-sanctions-screen.md`) | Przed bookingiem. S27b: M-13 snapshot z won/lost |
| **S27b** | Żywe **M-13** karta z decyzji oferty | 120.0 | zamknięty (`docs/deltas/archived/120.0-scorecard-offer-outcomes.md`) | Przyjęte/odrzucone S11. Nie scoring osoby. Nie zapis KPI |
| **S28** | Żywe **M-35** tabela `shipment` (= M-89 default) | 90.0 | zamknięty (`docs/deltas/archived/90.0-shipment-table.md`) | Tablica wycen ≠ zlecenie |
| **S29** | Żywe **M-36** zdarzenia trackingu | 91.0 | zamknięty (`docs/deltas/archived/91.0-tracking-event.md`) | Nie mapa w paczce JS |
| **S30** | Żywe **M-38** + arch. M-205 dokumenty | 92.0 | zamknięty (`docs/deltas/archived/92.0-shipment-document.md`) | Skan = M-20 |
| **S31** | Żywe **M-37** tabela wyjątków | 93.0 | zamknięty (`docs/deltas/archived/93.0-operational-exception.md`) | Nie filtr wycen bez POL/POD |
| **S32** | Watchtower UI (lista + S11 + lazy mapa) | 94.0 · 124.0 | zamknięty (`docs/deltas/archived/124.0-watchtower-tiles.md`) | Nie leaflet. AIS leftover |
| **S33** | Żywe **M-39** EDI gdy partner | 95.0 | zamknięty (`docs/deltas/archived/95.0-edi-message.md`) | Nie parser. Nie live HTTP |
| **S34** | Żywe **M-40** faktura | 96.0 | zamknięty (`docs/deltas/archived/96.0-sales-invoice.md`) | Fakturujesz zlecenie. Nie KSeF |
| **S35** | KSeF (osobny plaster) | 97.0 | zamknięty (`docs/deltas/archived/97.0-ksef-ref.md`) | Numer sesji, nie live HTTP |
| **S36** | Żywe **M-41** rozliczenie | 98.0 | zamknięty (`docs/deltas/archived/98.0-quote-invoice-settlement.md`) | Wiąże wycenę z fakturą. Nie druga marża |
| **S37** | Żywe **M-42** bank | 99.0 | zamknięty (`docs/deltas/archived/99.0-bank-payment.md`) | Faktura na rachunek. Nie SEPA. Nie druga marża |
| **S38** | Żywe **M-43** koszt pieniądza | 100.0 | zamknięty (`docs/deltas/archived/100.0-money-cost.md`) | Płatność przy kursie NBP. Nie odsetki. Nie mnożenie |
| **S39** | Żywe **M-44** różnice kursowe | 101.0 | zamknięty (`docs/deltas/archived/101.0-fx-difference.md`) | Wycena przy kursie NBP. Nie przeliczenie |
| **S40** | Żywe **M-45** przepływy | 102.0 | zamknięty (`docs/deltas/archived/102.0-cash-flow.md`) | Wycena przy płatności. Nie księga kwot. Nie odejmowanie |
| **S41** | Żywe **M-46** koszt obsługi | 103.0 | zamknięty (`docs/deltas/archived/103.0-cost-to-serve.md`) | SOP przy wycenie. Nie ABC. Nie suma |
| **S42** | Żywe **M-47** księgowość | 104.0 | zamknięty (`docs/deltas/archived/104.0-bookkeeping.md`) | Opłata na fakturę. Nie JPK. Nie odejmowanie |
| S43 | Arch. M-91 zbiorcze FV | 105.0 | zamknięty (`docs/deltas/archived/105.0-collective-invoice.md`) | Dodatkowe zlecenie na FV. Nie płatność paczką. Nie JPK |
| S44 | Żywe **M-15** tablica faktów (teraz z FV) | 106.0 | zamknięty (`docs/deltas/archived/106.0-finance-board-invoices.md`) | FV na `/finance`. Nie narracja. Nie silnik limitu |
| S45 | Żywe **M-56** wniosek/usuwanie RODO | 107.0 | zamknięty (`docs/deltas/archived/107.0-gdpr-request.md`) | Wniosek na `/gdpr`. Nie DPIA. Nie kasowanie innych BC |
| S46–S49 | M-48…M-51 obiekt nogi | 108.0 · 109.0 · 110.0 · 111.0 | zamknięte | Nie druga mapa. S50 leftover |
| S50 | Arch. M-111 flota | 112.0 park | named park (`docs/deltas/archived/112.0-fleet-named-park.md`) | Brak jobu „własne auto”. Nie TMS |
| S51 | Żywe **M-55** reklamacja | 113.0 | zamknięty (`docs/deltas/archived/113.0-cargo-claim.md`) | Reklamacja na zleceniu. Nie kwota. Nie scoring |
| S52 | Kat. M-54 oszustwo | 114.0 | zamknięty (`docs/deltas/archived/114.0-fraud-flag.md`) | Flaga na kontrahencie. Nie scoring osoby |
| **S53** | M-04 / Auth0 | 270.0 | zamknięty (`docs/deltas/archived/270.0-idp-connector.md`) | HITL `idp_connector` fixture; JWT hello zostaje; live I1/I2 parked. Przed portalami. 2026-09-13: Cloudflare Access (VISION B.8) ≠ Auth0 I1/I2 i **nie** zdejmuje tego leftoveru; park live public — nie Q `/noc` |
| S54 | Arch. M-76 status klienta | 115.0 park | named park (`docs/deltas/archived/115.0-client-status-named-park.md`) | Aż Auth0 S53. Nie wieża operatora |
| **S55** | F10 M-61…M-67, M-73, M-199 | 271.0 | zamknięty (`docs/deltas/archived/271.0-exchange-connector.md`) | HITL `exchange_connector` fixture `trans_eu`; giełda live parked |
| **S56** | Pogłębienie M-57 (kat. M-58) | 116.0 | zamknięty (`docs/deltas/archived/116.0-copilot-watchtower.md`) | Szkice na wieży. Nie nowy czat |
| S57 | Kat. M-59 narracja po SQL | 117.0 | zamknięty (`docs/deltas/archived/117.0-finance-narrative.md`) | Zdania z pól SQL. LLM nie liczy |
| S58 | Kat. M-60 drafty po SOP | 118.0 | zamknięty (`docs/deltas/archived/118.0-sop-drafts.md`) | SOP `blocks_auto` na `/ai`. Nigdy auto-send |
| S59 | M-68 OTel, M-69 QA, M-70 rollout | 119.0 park | named park (`docs/deltas/archived/119.0-otel-rollout-named-park.md`) | Aż konsument outboxa / umowa SaaS. Nie k6. 2026-09-13: edge Cloudflare / publikacja HTTP parked (VISION B.8). [WYCOFANE 2026-09-13: „nie zdejmuje 431.0” jako next-ID — **431.0** jest w kodzie] |

Po S59 named parks **live** (S53 Auth0, S55 ogólnik portali, S21, S50, S54, S59, AIS) czekają na swoje Q w CURRENT. Katalog 71–212 wpinany gdy jest poprzednik (cło/WMS po C/D; fintech po F). Luki **M-203, M-204** puste — nie zgaduj.

Pin operatora **2026-09-08c** (akceptacja „Luki i ulepszenia”): **nic nie wypada**. Oś:

`P0 → O0 → M10-1/M10-2 → B0a → O1–O3 → I0/U2 → O4–O8 → N5 → U1+U5 → I1–I4 → U4 → T1–T8 → B0b → U3 → D1–D9 → P1–P6 → G2.0–G2.23 → F1–F11 → C1–C9 → V1–V8 → W1–W5 → S53 → X1–X9 → WA1 → Plat (+Plat-HD) → Demo-1 → CT1–CT12 → CI9 → CI1–CI8 → G1+G3–G17 → EXP2–EXP8 (co nie wkleiło się w falę) → Mob → K0 → Fala AI → Fala BR`

Klej (nie osobny rok): **U6** + **M-72** = DoD każdego UI; **N** i **A** wchodzą z falą w kolumnie „Gdzie”; **EXP0/EXP1** = pola przy `/plan-modul` obiektu. Fala **X** i **Mob** po **S53**. `/noc` nie zgaduje S53 przy cutoffie T3; S53 rusza gdy CURRENT dojdzie do tego wiersza. Park = brak testu HTTP / sekretu na **live**, nie skip leftoveru HITL.

### Oś leftoverów `/noc` (przyczyna, nie skip)

Kolejka żywa jest w [CURRENT.md](state/CURRENT.md). `/noc` jedzie ją bez wycinania. Godzina ucina **nowy** plaster, nie wiersz pinu. Rzeka T3→CI9 (dziennik nocy, nie „co dalej”): [PLAN-HISTORIA.md](state/PLAN-HISTORIA.md).

Bliźniak = wzorzec (stan RLS + `entity_event` + opcjonalnie kopia planu / karta komunikacji), nie druga tabela `*_twin`. Rodziny rosną katalogiem. AI szuka i proponuje; `operator_decision` zamyka. LLM nie liczy.

Protokół nocy: [nocna-zmiana.md](ops/nocna-zmiana.md). Lista API operatora: [api-dostawy-operatora.md](ops/api-dostawy-operatora.md). Mapa funkcji: [konkurencja-funkcje-2026-09.md](analysis/konkurencja-funkcje-2026-09.md).

Karty: [karty-pol-fala-o.md](analysis/karty-pol-fala-o.md) · [i](analysis/karty-pol-fala-i.md) · [u](analysis/karty-pol-fala-u.md) · [n](analysis/karty-pol-fala-n.md) · [a](analysis/karty-pol-fala-a.md) · [t](analysis/karty-pol-fala-t.md) · [d](analysis/karty-pol-fala-d.md) · [p](analysis/karty-pol-fala-p.md) · [f](analysis/karty-pol-fala-f.md) · [c](analysis/karty-pol-fala-c.md) · [v](analysis/karty-pol-fala-v.md) · [w](analysis/karty-pol-fala-w.md) · [x](analysis/karty-pol-fala-x.md) · [g](analysis/karty-pol-fala-g.md) · [g2](analysis/karty-pol-g2-tender.md) · [ci](analysis/karty-pol-fala-ci.md) · [ct](analysis/karty-pol-fala-ct.md) · [plat](analysis/karty-pol-fala-plat.md) · [exp](analysis/karty-pol-fala-exp.md). Pola: [pola-wizja-2026-09.md](analysis/pola-wizja-2026-09.md).

Reguły: tabela+RLS przed HTTP; TO_VERIFY = park, nie teatr API; WIP=1; `/plan-modul` potem `/plaster`; LLM nie liczy; HITL zostaje; `charge` = marża; umowy CI = CI9 (zero AI w API operatora tenanta; SuperAdmin ma pełny dostęp poza tym API — decyzja 13 IX); zakaz scrapingu; zakaz copy „8 min / 15k userów / 500k od ręki / −12% Bayer jako nasza liczba”.

### Leftover P0 + M10 + B0a + Fala O + Fala I — **następna oś**

Pogłębienie żywych M-07/M-08 (`source_ref`), M-10, M-12, M-13, M-19, M-20, M-30, M-31, M-57. Nie nowy numer M-xx. Nie M-51 LCL.

| ID | Co | Tryb | Status | Zależności / poza zakresem |
|---|---|---|---|---|
| **P0** | `charge.source_ref` (nullable stare fixture; obowiązkowe na nowym INSERT) | Plan → plaster | zamknięty (`docs/deltas/archived/129.0-charge-source-ref.md`) | HC-05. Migracja 072. Nie backfill |
| **O0** | `network_member.party_id` FK tenanta | Plan → plaster | zamknięty (`docs/deltas/archived/130.0-network-member-party.md`) | FK tenanta. 409 rankingu = O3 |
| **M10-1** | Dedup NIP/VAT-EU/EORI/DUNS + wymóg ID biznesowego | Plan → plaster | zamknięty (`docs/deltas/archived/131.0-party-business-ids.md`) | 409 z linkiem. Zakaz B2C bez NIP |
| **M10-2** | `party_role_assignment` + JDG + `parent_party_id` | Plan → plaster | zamknięty (`docs/deltas/archived/132.0-party-roles-jdg.md`) | JDG → kredyt HITL. Agent/armator/podwykonawca = role, nie trzy tabele |
| **B0a** | `entity_event` append-only | Plan → plaster | zamknięty (`docs/deltas/archived/133.0-entity-event.md`); leftover 2a [244.0](deltas/archived/244.0-inquiry-queued-event.md); leftover 2b [245.0](deltas/archived/245.0-inquiry-sent-event.md); leftover `quote_recorded` [246.0](deltas/archived/246.0-quote-recorded-event.md); leftover POST `channel_quote` | Kind: `inquiry_queued` / `inquiry_sent` / `quote_recorded`. 2a = compose z API. Ledger/what-if = B0b po T2 |
| **O1** | `channel_quote.transit_days` + znaczki najtańsza / najszybszy TT (SQL, ta sama waluta) | Plan → plaster | zamknięty (`docs/deltas/archived/134.0-channel-quote-transit.md`) | Nie mnożenie NBP (T7). UI `/quotations` |
| **O2** | Ręczny POST `channel_quote` z wyceny (`source_ref=tenant:manual:`) | Plan → plaster | zamknięty (`docs/deltas/archived/135.0-channel-quote-from-quote.md`) | Nie mutacja stawki. Nie 1.3 `rate_line` w tym wierszu |
| **O3** | `carrier_inquiry` batch; statusy `queued`/`sent`/`answered`/`declined`; lane POL/POD | Plan → plaster | zamknięty (`docs/deltas/archived/136.0-carrier-inquiry-batch.md`) | Wskazanie wyceny w API, nie import serwisu. 1 / wielu / wszyscy |
| **O4** | Checkboxy + default N z M-03; N× `mail_draft`; ranking SQL | Plan → plaster | zamknięty (`docs/deltas/archived/138.0-inquiry-mail-draft-batch.md`) | Send = S18 po S11. Zakaz auto-send. Graph HTTP leftover |
| **O5** | `party_lane_scorecard` + szablon podpowiedzi z SQL | Plan → plaster | **delta 139.0 zaakceptowana** | `sample_size=0` i tak ma tekst. Nie LLM. Nie scoring osoby |
| **O6** | `extraction_draft.draft_kind=carrier_quote` → HITL → `channel_quote` + `answered` | Plan → plaster | zamknięty leftover HITL ([531.0](deltas/archived/531.0-carrier-quote-hitl.md); leftover `quote_recorded` przy accept [534.0](deltas/archived/534.0-quote-recorded-on-accept.md)) | ExtractionService nie zapisuje stawek |
| **O7** | Kraj ISO na liście agentów (`party.country_code` już jest) + filtr | Plan → plaster | zamknięty ([532.0](deltas/archived/532.0-agent-country-filter.md); EXPLAIN [535.0](deltas/archived/535.0-buy-desk-explain.md)) | Holandia na SHA→RTM. Nie druga kolumna kraju |
| **O8** | Buy-desk: group-by edytowalny (party/kraj/wątek/status) + saved view | Plan → plaster | zamknięty ([533.0](deltas/archived/533.0-buy-desk-groupby.md); EXPLAIN [535.0](deltas/archived/535.0-buy-desk-explain.md); rfc822 [536.0](deltas/archived/536.0-inbound-rfc822.md); `/mail` thread [538.0](deltas/archived/538.0-mail-thread-groupby.md)) | leftover buy-desk po rfc822 · live Graph |
| **N5** | Cisza agenta: SLA `no_reply_after` (U4 dni robocze) → notice | Plan → plaster | zamknięty (`docs/deltas/archived/143.0-inquiry-no-reply.md`) | nie auto-send ponaglenia |

### Fala U — klej oferty i UI (w osi, nie leftover)

Karta: [karty-pol-fala-u.md](analysis/karty-pol-fala-u.md). **U6** + **M-72** = DoD każdego ekranu (nie osobny rok).

| ID | Co | Tryb | Status | Poza |
|---|---|---|---|---|
| **I0 / U2** | `quotation.incoterm` + `trade_side` + `named_place` + wersja 2020/2010 | Plan → plaster | zamknięty (`docs/deltas/archived/137.0-quotation-incoterm.md`) | DAP bez miejsca = 409; nie cytat ICC |
| **U1** | `field_carry_forward` oferta→zlecenie→booking→FV; diff przy POST | zamknięty (`docs/deltas/archived/144.0-u1-u5-carry-checklist.md`) | po O8, przed I1 | mutacja = nowy wiersz / `superseded_by` |
| **U5** | `document_checklist_rule` (incoterm×side×mode) + `blocks_dispatch` | zamknięty (z U1, 144.0) | z U1 | ≠ C8 polisa podwykonawcy |
| **U4** | `organization_calendar` + `is_working_day`; grace V5 = 3 dni **robocze** | zamknięty (`docs/deltas/archived/149.0-organization-calendar.md`) | po I4, przed T1 | nie `+3` kalendarzowe |
| **U3** | `shipment_leg.kind=air` HAWB/MAWB + pule; lotnisko = `port` air | zamknięty ([154.0](deltas/archived/154.0-air.md); leftover U3b HAWB/MAWB [209.0](deltas/archived/209.0-air-hawb.md); leftover U3c pule [619.0](deltas/archived/619.0-air-waybill-pools.md); leftover e-rates [620.0](deltas/archived/620.0-air-channel-erate.md); leftover cyfra kontrolna IATA [622.0](deltas/archived/622.0-mawb-iata-check.md)) | po T, przed D | nie live IATA bez umowy |
| **N9** | F2 + klon ostatniego podobnego zlecenia | zamknięty HITL intencja ([528.0](deltas/archived/528.0-shipment-clone-mark.md); leftover clone U1 carry → **631.0** `clone_carry_mark` HITL DONE; park auto-copy / similar SQL / F2b) | z U1 | nie drugi SoR |

### Fala I — Incoterms, booking, odprawa (po U1; zlecenie już jest)

Macierz = **dane**. LLM nie wybiera adresata. Send jak O4. Audyt: [incoterms-booking-customs-ux.md](analysis/incoterms-booking-customs-ux.md). Karta: [karty-pol-fala-i.md](analysis/karty-pol-fala-i.md).

| ID | Co | Tryb | Status | Poza |
|---|---|---|---|---|
| **I1** | `incoterm_responsibility` (11 reguł × import/export) | zamknięty (`docs/deltas/archived/145.0-incoterm-responsibility.md`) | po U1+M10-2 | nie cytat ICC; seed ops Omni |
| **I2** | `shipment_stakeholder` + EXP1: sold_to / bill_to / ship_to / notify | zamknięty (`docs/deltas/archived/146.0-shipment-stakeholder.md`) | po I1 | 409 dispatch bez party |
| **I3** | `document_dispatch_rule` + batch mail dokumentów odprawy | zamknięty (`docs/deltas/archived/147.0-document-dispatch-rule.md`) | po I2+O4 | nie auto-send; nie Selenium celny |
| **I4** | `booking_instruction` (scope + target z macierzy; DAP = contact_exchange) | zamknięty (`docs/deltas/archived/148.0-booking-instruction.md`) | po I2 | nie live HTTP S21; accept człowieka |

### Fala T — warstwa wykonawcza (pełna, nie szkic)

Przy `/plan-modul`: karta T + [EXP1](analysis/karty-pol-fala-exp.md) (stop/kontener/role). N1/N4/N10/N11 wklejone.

| ID | Co | Tryb | Status | Poza |
|---|---|---|---|---|
| T1 | `stop` + `stop_group` + timezone + `eta_physical`/`eta_legal` + EXP1 (awizacja, plomba, waga, waiting, POD quality) | zamknięty punkt ([150.0](deltas/archived/150.0-stop.md)); ETA HITL ([194.0](deltas/archived/194.0-stop-eta.md)); leftover `stop_group` kolumna [213.0](deltas/archived/213.0-stop-group.md); leftover T1 `notes_for_driver` [215.0](deltas/archived/215.0-stop-notes-for-driver.md); leftover T1 EXP1 `weight_kg` [247.0](deltas/archived/247.0-stop-weight.md); leftover T1 EXP1 `quantity` [248.0](deltas/archived/248.0-stop-quantity.md); leftover T1 EXP1 `packaging_code` [249.0](deltas/archived/249.0-stop-pack.md); leftover T1 EXP1 `seal_in` [250.0](deltas/archived/250.0-stop-seal-in.md); leftover T1 EXP1 `seal_out` [251.0](deltas/archived/251.0-stop-seal-out.md); leftover T1 EXP1 `appointment_ref` [252.0](deltas/archived/252.0-stop-appointment-ref.md); leftover T1 EXP1 `waiting_free_minutes` [253.0](deltas/archived/253.0-stop-waiting.md); leftover EXP1 `waiting_started_at` [254.0](deltas/archived/254.0-stop-waiting-started.md); leftover EXP1 POD (`pod_quality`) [255.0](deltas/archived/255.0-stop-pod-quality.md); leftover T1b tabela [600.0](deltas/archived/600.0-stop-group-table.md); leftover T1b bind [601.0](deltas/archived/601.0-stop-group-bind.md); leftover T1b sync [602.0](deltas/archived/602.0-stop-group-sync.md); leftover EXP1 appointment_status [603.0](deltas/archived/603.0-stop-appointment-status.md); leftover EXP1 no_show_at [604.0](deltas/archived/604.0-stop-no-show-at.md); leftover EXP1 weigh_in_kg [605.0](deltas/archived/605.0-stop-weigh-in.md); leftover EXP1 weigh_out_kg [606.0](deltas/archived/606.0-stop-weigh-out.md) | po U4 | nie mapa |
| **N1** | `consignment` obok `shipment` | zamknięty HITL ([260.0](deltas/archived/260.0-consignment.md); FTL=1 409 [540.0](deltas/archived/540.0-consignment-ftl-409.md); D2b FK paczki [541.0](deltas/archived/541.0-package-consignment-fk.md); stop [542.0](deltas/archived/542.0-consignment-stop.md); leftover auto-link / mapa) | po T1, przed D2 | leftover auto-link / mapa; LTL/LCL=N |
| T2 | `trip` + `resource`; floating trailer; multi-manning | zamknięty (`resource` [151.0](deltas/archived/151.0-resource.md); `trip` [152.0](deltas/archived/152.0-trip.md); leftover T2c `driver2` [212.0](deltas/archived/212.0-trip-driver2.md); leftover T2 `route_label` [214.0](deltas/archived/214.0-trip-route-label.md); leftover T2c `planned_distance_km` [256.0](deltas/archived/256.0-trip-planned-distance.md); leftover T2c `actual_distance_km` [257.0](deltas/archived/257.0-trip-actual-distance.md); leftover T2c `subcontractor_party_id` [258.0](deltas/archived/258.0-trip-subcontractor.md); leftover T2c `/fleet` [259.0](deltas/archived/259.0-fleet-route.md); leftover T2 `capacity_kg` [589.0](deltas/archived/589.0-resource-capacity-kg.md); leftover T2 `capacity_ldm` [590.0](deltas/archived/590.0-resource-capacity-ldm.md); leftover T2 `capacity_m3` [591.0](deltas/archived/591.0-resource-capacity-m3.md); leftover T2 `document_expiries` [592.0](deltas/archived/592.0-resource-document.md); leftover T2 `inventory_no` [593.0](deltas/archived/593.0-resource-inventory-no.md); leftover T2 `adr_certified` [594.0](deltas/archived/594.0-resource-adr-certified.md); leftover T2 `reefer` [595.0](deltas/archived/595.0-resource-reefer.md); leftover T2 `tail_lift` [596.0](deltas/archived/596.0-resource-tail-lift.md); leftover T2 `phone` [597.0](deltas/archived/597.0-resource-phone.md); leftover T2 `driver_card_no` [598.0](deltas/archived/598.0-resource-driver-card-no.md); leftover T2 `vehicle_profile` [599.0](deltas/archived/599.0-resource-vehicle-profile.md); leftover HW) | po T1 | nie własne HW; job S50 · leftover HW |
| T3 | `container` ISO + EXP1 (VGM, free time, BL kind, cutoffy CY/CFS/VGM/SI/AMS) | zamknięty ([153.0](deltas/archived/153.0-container.md); leftover T3 `seal_no_1` [216.0](deltas/archived/216.0-container-seal.md); leftover T3 `seal_no_2` [217.0](deltas/archived/217.0-container-seal2.md); leftover T3 `seal_no_3` [218.0](deltas/archived/218.0-container-seal3.md); leftover T3 `vessel_name` [219.0](deltas/archived/219.0-container-vessel.md); leftover T3 `voyage_no` [220.0](deltas/archived/220.0-container-voyage.md); leftover T3 `remarks` [221.0](deltas/archived/221.0-container-remarks.md); leftover T3 `cargo_description` [222.0](deltas/archived/222.0-container-cargo.md); leftover T3 `packaging_code` [223.0](deltas/archived/223.0-container-pack.md); leftover T3 `ref_1` [224.0](deltas/archived/224.0-container-ref1.md); leftover T3 `ref_2` [225.0](deltas/archived/225.0-container-ref2.md); leftover T3 `ref_3` [226.0](deltas/archived/226.0-container-ref3.md); leftover T3 `ref_4` [227.0](deltas/archived/227.0-container-ref4.md); leftover T3 `ref_5` [228.0](deltas/archived/228.0-container-ref5.md); leftover T3 `reefer` [229.0](deltas/archived/229.0-container-reefer.md); leftover T3 `pickup_terminal` [230.0](deltas/archived/230.0-container-pickup-terminal.md); leftover T3 `return_terminal` [231.0](deltas/archived/231.0-container-return-terminal.md); leftover T3 `bl_kind` [232.0](deltas/archived/232.0-container-bl-kind.md); leftover T3 `free_time_origin_h` [233.0](deltas/archived/233.0-container-free-time-origin.md); leftover T3 `free_time_dest_h` [234.0](deltas/archived/234.0-container-free-time-dest.md); leftover T3 `si_cutoff_at` [235.0](deltas/archived/235.0-container-si-cutoff.md); leftover T3 `ams_cutoff_at` [236.0](deltas/archived/236.0-container-ams-cutoff.md); leftover T3 `cy_cutoff_at` [237.0](deltas/archived/237.0-container-cy-cutoff.md); leftover T3 `cfs_cutoff_at` [238.0](deltas/archived/238.0-container-cfs-cutoff.md); leftover T3 VGM bundle [239.0](deltas/archived/239.0-container-vgm.md); leftover T3 `last_survey_at` [240.0](deltas/archived/240.0-container-last-survey.md); leftover T3 `booking_no` [241.0](deltas/archived/241.0-container-booking-no.md); leftover T3 `carrier_party_id` [242.0](deltas/archived/242.0-container-carrier-party.md); leftover T3 `shipment_leg_id` [243.0](deltas/archived/243.0-container-shipment-leg.md); leftover T3 `tare_kg` [569.0](deltas/archived/569.0-container-tare-kg.md);  leftover T3 EXP1 `vessel_imo` [608.0](deltas/archived/608.0-container-vessel-imo.md); leftover T3 EXP1 `alliance_service` [609.0](deltas/archived/609.0-container-alliance-service.md); leftover T3 `pol_unlocode` [610.0](deltas/archived/610.0-container-pol-unlocode.md); leftover T3 `pod_unlocode` [611.0](deltas/archived/611.0-container-pod-unlocode.md); leftover T3 `destination_city` [612.0](deltas/archived/612.0-container-destination-city.md)) | po T1 | nie booking armatorski |
| T4 | `parent_shipment_id`; rentowność SQL na `charge` | zamknięty HITL ([210.0](deltas/archived/210.0-shipment-parent.md); leftover T4b SQL lista ([262.0](deltas/archived/262.0-charge-sql-margin.md)); leftover wnuki — widok korzeń+dzieci [614.0](deltas/archived/614.0-shipment-tree-margin.md)) | po T1 | nie druga marża |
| T5 | task engine (warunki = dane) | zamknięty HITL szablon ([263.0](deltas/archived/263.0-task-template.md); leftover outbox kind ([264.0](deltas/archived/264.0-outbox-task-template.md)); HITL instancja `task` [616.0](deltas/archived/616.0-task.md); leftover matching SQL / FK kontekstu / konsument) | po T2 | async po konsumencie outboxa (leftover M-02) |
| T6 | planning board 4 widoki + mapa lazy + klawiatura N10 | zamknięty HITL mapa ([261.0](deltas/archived/261.0-planning-map.md); leftover 4 widoki / N10 / T6b–d / X8) | po T2 | mapa poza 250 kB |
| **N11** | handover SBAR zmiany | zamknięty HITL ([529.0](deltas/archived/529.0-handover-sbar-mark.md); notatka S/B/A/R [543.0](deltas/archived/543.0-handover-note.md); bind stance [637.0](deltas/archived/637.0-handover-bind-mark.md); leftover T6 live · N8 · auto SBAR) | po T6 | leftover T6 live · N8 · auto SBAR |
| T7 | `fx_rate_basis` SQL; kalendarz U4 | zamknięty HITL ([211.0](deltas/archived/211.0-fx-rate-basis.md); leftover T7b override/`charge` [615.0](deltas/archived/615.0-charge-fx-rate.md); T7c `fx_rate_day` [617.0](deltas/archived/617.0-fx-working-day.md); T7d SQL `charge_sell_in_pln` [618.0](deltas/archived/618.0-charge-fx-sql.md); daty bazowe [628.0](deltas/archived/628.0-shipment-fx-anchor-dates.md); leftover fx×FV) | po T1+U4 | LLM/JS nie liczą |
| T8 | slot capability + godziny terminalu N4; **confirmed tylko z API** | zamknięty HITL ([269.0](deltas/archived/269.0-terminal-slot-connector.md); leftover live API / `terminal_appointment` / confirmed z adaptera) | po T3 | nie gwarancja prawna; nie Selenium |

**B0b** (po T2): zamknięty HITL `prediction_ledger` + N7 ([193.0](deltas/archived/193.0-prediction-ledger.md)); zamknięty HITL `plan_snapshot` ([265.0](deltas/archived/265.0-plan-snapshot.md)); zamknięty HITL `circle_sim` ([266.0](deltas/archived/266.0-circle-sim.md)); zamknięty HITL `lane_km` ([267.0](deltas/archived/267.0-lane-km.md)); leftover TT z actuals — karta [karty-pol-fala-v.md](analysis/karty-pol-fala-v.md). Indeks paliwa = P3 `fuel_index`.

**N / A w T:** N9 z U1; A3/A6/A7/A9/A14/A17 przy T — karta [karty-pol-fala-n.md](analysis/karty-pol-fala-n.md) · [a](analysis/karty-pol-fala-a.md).

### Fala D — drobnica / LTL (pełna)

| ID | Co | Status | Uwagi |
|---|---|---|---|
| D1–D7 | linie, paczka, cross-dock, COD, cennik LTL, LCL/HBL, palety Chep/LPR (EXP2.17) | D1 zamknięty ([155.0](deltas/archived/155.0-groupage-line.md); leftover OR hubów); D2 zamknięty ([156.0](deltas/archived/156.0-shipment-package.md); leftover kamera/WMS/SSCC); D3 zamknięty ([157.0](deltas/archived/157.0-dock-appointment.md); leftover D3b/G15/T8); D4 zamknięty ([158.0](deltas/archived/158.0-cod-instruction.md); leftover D4b POD/ROD [624.0](deltas/archived/624.0-shipment-document-rod.md)); D5 zamknięty ([159.0](deltas/archived/159.0-groupage-tariff.md); leftover D5b objętość [625.0](deltas/archived/625.0-groupage-tariff-volume.md) / P1); D6 zamknięty ([160.0](deltas/archived/160.0-ocean-bill.md); leftover D6b; leftover D6c pule M-03 [621.0](deltas/archived/621.0-ocean-bill-pools.md)); D7 zamknięty ([161.0](deltas/archived/161.0-pallet-balance.md); leftover D7b giełda park live; leftover D7c ledger [629.0](deltas/archived/629.0-pallet-ledger.md); leftover D7c synchro [630.0](deltas/archived/630.0-pallet-synchro-mark.md); leftover D7d EPAL [623.0](deltas/archived/623.0-pallet-balance-epal.md)) | po U3+T2; nie WMS; karta [karty-pol-fala-d.md](analysis/karty-pol-fala-d.md) |
| D8 | etykieta sieci po oficjalnym API | parked aż TO_VERIFY API | zakaz generatora Palletforce |
| D9 | silnik wydruków + QR `shipment_ref` | zamknięty ([162.0](deltas/archived/162.0-document-template.md); leftover D9b HITL numer ([204.0](deltas/archived/204.0-shipment-ref.md)); leftover D9c katalog ([626.0](deltas/archived/626.0-network-print-requirement.md)); leftover D9f branding ([627.0](deltas/archived/627.0-document-template-branding.md)); leftover D9c 409 stance ([632.0](deltas/archived/632.0-network-print-gate-mark.md)); leftover D9f rest `output_kind` HITL ([636.0](deltas/archived/636.0-document-template-output-kind.md)); leftover D9d–e / D9f pdf-zpl live / live 409) | live 409 / PDF park; D8 parked |

### Fala P — pricing (P1–P6; P0 wyżej)

| ID | Co | Status | Uwagi |
|---|---|---|---|
| P1–P3 | rate card / szablony / FSC + indeks BAF/CAF (EXP1) + A11 nowy wiersz | P1 zamknięty ([163.0](deltas/archived/163.0-rate-card.md); leftover P1b matching GET ([205.0](deltas/archived/205.0-rate-card-match.md)); leftover P1c–d); P2 zamknięty ([164.0](deltas/archived/164.0-charge-template.md); leftover P2c exclusion daterange ([206.0](deltas/archived/206.0-charge-template-span.md))); P3 zamknięty ([165.0](deltas/archived/165.0-fuel-index.md); leftover P3b–d) | po T7 + M-18; dane + SQL; nie T-SQL |
| **N6** | `margin_floor` per tenant/lane → 409 albo S11 | zamknięty HITL ([527.0](deltas/archived/527.0-margin-floor.md); 409 API [539.0](deltas/archived/539.0-margin-floor-409.md); S11 [544.0](deltas/archived/544.0-margin-floor-s11.md); UI UN [547.0](deltas/archived/547.0-charges-un-ui.md); leftover matching stance → **639.0** DONE; leftover auto charge park) | Decimal; nie LLM |
| P4 | Local Charge Library + THC/ISPS/seal/amendment (EXP4.5) + warning | zamknięty ([166.0](deltas/archived/166.0-local-charge.md); leftover P4b `port_unlocode` ([207.0](deltas/archived/207.0-local-charge-port.md)); leftover P4b rest `iso_size_type` ([208.0](deltas/archived/208.0-local-charge-iso.md)); leftover P4b armator/serwis ([633.0](deltas/archived/633.0-local-charge-carrier-service.md)); leftover P4c warning stance ([635.0](deltas/archived/635.0-local-charge-warning-mark.md)); leftover P4c matching stance ([640.0](deltas/archived/640.0-local-charge-match-mark.md)); leftover P4c bind stance ([641.0](deltas/archived/641.0-local-charge-bind-mark.md)); leftover warning-jako-fakt park) | po O2; warning ≠ fakt |
| P5 | expected vs actual na `trip` | zamknięty ([167.0](deltas/archived/167.0-trip-expected-buy.md); leftover P5b variance stance → **638.0** DONE; leftover P5c actual-from-charge park) | po T2; nie druga marża |
| P6 | tender quotes (buy) | zamknięty ([168.0](deltas/archived/168.0-tender-quote.md); leftover P6b–c) | po M-25; nie auto-award; klej G2 |

### G2 — Tender desk Enterprise (sell + buy; po P)

Karta: [karty-pol-g2-tender.md](analysis/karty-pol-g2-tender.md). P6 = oferty od podwykonawców. G2 = obiekt `tender`.

| ID | Co | Status | Poza |
|---|---|---|---|
| G2.0 | obiekt `tender` (nagłówek sell+buy) | zamknięty ([169.0](deltas/archived/169.0-tender.md); leftover G2.2–G2.18) | po P6; nie loty; nie auto-award |
| G2.1 | partia `tender_lot` | zamknięty ([170.0](deltas/archived/170.0-tender-lot.md); leftover G2.3–G2.18) | po G2.0; nie lane; nie kwota |
| G2.2 | korytarz `tender_lane` | zamknięty ([171.0](deltas/archived/171.0-tender-lane.md); leftover G2.4–G2.18) | po G2.1; nie runda; nie kwota |
| G2.3 | runda `tender_round` | zamknięty ([172.0](deltas/archived/172.0-tender-round.md); leftover G2.4–G2.18) | po G2.2; nie data room; nie kwota |
| G2.4 | pokój `tender_data_room` (NDA jako dane) | zamknięty ([173.0](deltas/archived/173.0-tender-data-room.md); leftover G2.5–G2.18) | po G2.3; nie extract; nie bajty; nie kwota |
| G2.5 | komórka `tender_matrix_cell` (kwota z P) | zamknięty ([174.0](deltas/archived/174.0-tender-matrix-cell.md); leftover G2.6–G2.18) | po G2.4; nie LLM kolumny; nie druga marża |
| G2.6 | playbook `tender_playbook` (twierdzenie + source_ref) | zamknięty ([175.0](deltas/archived/175.0-tender-playbook.md); leftover G2.7–G2.18) | po G2.5; nie extract RFP |
| G2.7 | win/loss `tender_win_loss` (wynik + source_ref) | zamknięty ([176.0](deltas/archived/176.0-tender-win-loss.md); leftover G2.8–G2.18) | po G2.6; nie extract RFP; nie four-eyes |
| G2.8 | konsorcjum `tender_consortium_member` (fotel + source_ref) | zamknięty ([177.0](deltas/archived/177.0-tender-consortium-member.md); leftover G2.9–G2.18) | po G2.7; nie extract RFP; nie TED |
| G2.9–G2.18 | extract RFP HITL, prospecting HITL, bid/no-bid, award four-eyes, TED capability, CO₂ | zamknięty intake ([178.0](deltas/archived/178.0-tender-rfp-intake.md)); zamknięty kind/accept ([179.0](deltas/archived/179.0-tender-rfp-draft-kind.md)); zamknięty prospect ([180.0](deltas/archived/180.0-tender-prospect.md)); zamknięty bid/no-bid ([181.0](deltas/archived/181.0-tender-bid-stance.md)); zamknięty four-eyes ([182.0](deltas/archived/182.0-tender-award-review.md)); zamknięty TED HITL ([183.0](deltas/archived/183.0-tender-ted-notice.md)); zamknięty CO₂ HITL ([184.0](deltas/archived/184.0-tender-carbon-mark.md)); leftover G2.15–G2.18 kg/CBAM | auto-award; scrape kontaktów |
| G2.19–G2.22 | `lane_pattern`, `circle_sim` ≥500k w Postgres, km ładowny/pusty/dolot, lista przewoźników | zamknięty HITL para UN/LOCODE ([185.0](deltas/archived/185.0-lane-pattern.md)); zamknięty HITL kółko ([266.0](deltas/archived/266.0-circle-sim.md)); zamknięty HITL km ładowny ([267.0](deltas/archived/267.0-lane-km.md)); leftover G2.22 P/lista / silnik 500k | LLM-VRP; copy „natychmiast” bez p95 stage |
| **G2.23** | KREPTD/GITD (ITD): P0 link+HITL; P1 Citizen API po certyfikacie; lead + C8 licencja | zamknięty HITL numer licencji ([186.0](deltas/archived/186.0-kreptd-licence.md)); leftover Citizen API / C8 `party_document` | scrape HTML kreptd; scoring osoby |

### Fala F — finanse głębiej (ID **F1–F11** bez kropki)

| ID | Co | Status | Uwagi |
|---|---|---|---|
| F1 | KSeF live FA(3) + VAT matrix N12 | po S35 | mandat 2026; nie LLM VAT; dump `04b`: KSeF/JPK nie publiczne u TMS top-10 — leftover fiskalne PL nasze |
| F2–F4 | skonto, noty, CAMT+HITL + period lock N13 | zamknięty HITL F2 katalog ([189.0](deltas/archived/189.0-cash-discount.md)); leftover Decimal / F3 noty / F4 CAMT | karta [karty-pol-fala-f.md](analysis/karty-pol-fala-f.md) |
| **N2** | `trips_to_bill` | zamknięty HITL ([530.0](deltas/archived/530.0-trip-bill-mark.md); leftover SQL trips×charge · F1 live) | po T2+F1 | leftover SQL trips×charge · F1 live |
| F5 / F7 | diety / faktoring | TO_VERIFY | nie LLM diet |
| F6 | windykacja + blokada zlecenia | po T2 | S11; zakaz auto art. 22 |
| **M14b** | Szkic oceny kredytowej | po M-14 | LLM nie liczy limitu |
| F8 | Peppol + MPP/split (EXP2.20) | kalendarz UE | nie zastępuje KSeF |
| F9 | `purchase_invoice` + ERP FS+FZ | zamknięty HITL catalog Optima fixture ([268.0](deltas/archived/268.0-erp-connector.md)); leftover XL / live SOAP / FS+FZ / `erp_series_map` / `erp_export` / `purchase_invoice` | zakaz SQL `sa` |
| **N14** | self-billing podwykonawcy | zamknięty HITL ([548.0](deltas/archived/548.0-self-billing-mark.md)); leftover live · FK party · JPK | po F9+D |
| F10 | ingest FV HITL + ranking SQL | zamknięty HITL ([549.0](deltas/archived/549.0-purchase-invoice.md)); [550.0](deltas/archived/550.0-invoice-match-mark.md); [551.0](deltas/archived/551.0-invoice-alloc-mark.md); zamknięty HITL candidate ([555.0](deltas/archived/555.0-invoice-match-candidate.md)); leftover ranking SQL / allocation z kwotą / FK purchase_invoice | po F9 + X9 |
| F11 | książka PP EN+USS+EPO | zamknięty HITL ([552.0](deltas/archived/552.0-postal-dispatch-mark.md)); leftover live PP / `postal_epo` | **≠ e-Doręczenia** (EXP2.19) |
| **EXP2.1** | working capital: DSO, cash-at-risk, aging | 338.0 HITL katalog `working_capital_mark` (capital_kind); leftover DSO SQL / druga marża | nie druga marża |

### Fala C — celna / compliance

| ID | Co | Status | Uwagi |
|---|---|---|---|
| C1 / C6–C8 | SENT, BDO, `monitoring_scheme`, `party_document` 409 + KREPTD C8 | zamknięty HITL C7 katalog ([187.0](deltas/archived/187.0-monitoring-scheme.md)); zamknięty HITL C8 katalog ([188.0](deltas/archived/188.0-party-document.md)); zamknięty HITL C1 ([553.0](deltas/archived/553.0-shipment-monitoring-filing.md)); zamknięty HITL bind ([558.0](deltas/archived/558.0-filing-bind-mark.md)); zamknięty HITL cel FK ([561.0](deltas/archived/561.0-filing-fk-mark.md)); leftover live FK UUID / PUESC; zamknięty HITL C8 leftover ([554.0](deltas/archived/554.0-relation-document-requirement.md)); zamknięty HITL brama create ([556.0](deltas/archived/556.0-create-block-mark.md)); zamknięty HITL egzekucja bramy ([560.0](deltas/archived/560.0-blocks-create-enforcement-mark.md)); leftover live 409 shipment / wiring; zamknięty HITL document_kind ([557.0](deltas/archived/557.0-document-kind-match-mark.md)); zamknięty HITL C6 `waste_mark` ([563.0](deltas/archived/563.0-waste-mark.md)); zamknięty HITL C6 `shipment.is_waste` ([564.0](deltas/archived/564.0-shipment-is-waste.md)); leftover MOS live | karta [karty-pol-fala-c.md](analysis/karty-pol-fala-c.md); dump `04b`: SENT nie publiczne u TMS top-10 |
| C2 | AIS/AES/Intrastat | zamknięty HITL katalog ([562.0](deltas/archived/562.0-ais-import-mark.md)); leftover PUESC live | TO_VERIFY konto PUESC |
| C3–C5 / C9 | lookup live, eCMR 2027 (EXP2.18), CO₂+metodyka, Trans.eu snapshot | zamknięty HITL C5 katalog ([190.0](deltas/archived/190.0-carbon-method.md)); leftover C3 live VIES/GUS / C4 eCMR / C9 Trans.eu | C9 bez scrapingu opinii |
| **EXP0.8** | `cargo_claim` deadline CMR 7/21/365 + OS&D | zamknięty HITL OS&D + terminy ([191.0](deltas/archived/191.0-cargo-claim-cmr.md)); leftover Deadline Engine / evidence / S11 | nie kwota z LLM |
| **EXP0.9** | UN: `adr_tunnel_code` + `segregation_group` | zamknięty HITL tunel ADR + SG ([192.0](deltas/archived/192.0-dangerous-good-adr.md)); packing group DONE **642.0**; marine pollutant DONE **643.0**; `limited_quantity` → **644.0**; leftover live IMO / grupy 1.xA park | LLM nie nadaje klasy |

### Fala V — predykcje / telematyka / wieża

| ID | Co | Status | Uwagi |
|---|---|---|---|
| V1 | Prediction Ledger + N7 przedział/kalibracja | zamknięty HITL CRPS/MAE ([193.0](deltas/archived/193.0-prediction-ledger.md)); leftover champion/challenger / drift | punkt bez CRPS = zakaz; dump CT `03`: p44 PLANNED/ACTUAL/ESTIMATE analog, vendor bez CRPS/MAE — leftover AI2 liczy; Triple SLA Shippeo ZA LOGOWANIEM, nie claimować; dump `04b`: Oracle LML 95% interval = metoda, nie CRPS; ledger HITL aż AI2 |
| V2 / V2b | ETA **dwa czasy** `eta_physical`/`eta_legal` + pogoda; myto → `charge`+`source_ref` | ETA HITL zamknięte ([194.0](deltas/archived/194.0-stop-eta.md)); pogoda HITL zamknięta ([195.0](deltas/archived/195.0-weather-observation.md)); leftover Open-Meteo / geometria / myto | brak taryfy = warning |
| V3 | D&D / rollover + zegar N3 + blank sailing EXP2.7 | zamknięty HITL katalog ([196.0](deltas/archived/196.0-free-time-clock.md)); zamknięty HITL blank sailing ([565.0](deltas/archived/565.0-blank-sailing-mark.md)); zamknięty HITL `demurrage_free_days` ([566.0](deltas/archived/566.0-container-demurrage-days.md)); zamknięty HITL `detention_free_days` ([567.0](deltas/archived/567.0-container-detention-days.md)); zamknięty HITL `mixed_dd_days` ([568.0](deltas/archived/568.0-container-mixed-dd-days.md)); leftover N3 countdown / szkic charge | |
| V4 | AIS wieży | leftover S32 | nie V5 |
| V5 / V5b | hub GPS; `omni_telematic` vs `external_api` 3 dni **robocze** (U4) | zamknięty HITL katalog ([197.0](deltas/archived/197.0-telematics-connector.md)); leftover `resource_telematics_link` / ciphertext / 3 dni U4 / V5b `exchange_message`; `position_event` HITL = **457.0** | zero własnego HW |
| V6 | wieża impact; bez `sla_clause` = „brak danych umowy” (EXP0.1 → CI5) | zamknięty HITL katalog ([198.0](deltas/archived/198.0-tower-impact.md)); leftover silnik EBITDA / `sla_clause` CI5 / V8 | nie scoring osoby; dump CT `03`: GTT planned+tolerance / unplanned / XRI — leftover silnik, otwarty słownik milestone (nie lista w kodzie) |
| V7 | tacho / posting; TO_VERIFY prawo | | apka nie poprawia firmware |
| V8 | what-if na `plan_snapshot` (paliwo/port/bankructwo) EXP2.10 | po B0b | nie „AI widzi wojnę”; dump `04b`: LML/Optimizer/Archer/what-if u konkurencji = runtime; u nas HITL aż AI4.1 |

### Fala W — twins / war room (po V)

Karta: [karty-pol-fala-w.md](analysis/karty-pol-fala-w.md).

| ID | Co | Status | Poza |
|---|---|---|---|
| W1 | 8 twinów (pojazd, kierowca, kontener, zlecenie, sieć, plan, urząd, ładunek) | zamknięty HITL katalog ([199.0](deltas/archived/199.0-twin-mark.md)); `plan_snapshot` DONE 265.0; `circle_sim` HITL DONE 266.0; leftover 8 silników | twin ≠ fizyka; kółka HITL = G2.20; dump CT `03`: leftover 8 silników zostaje (nie nowy katalog HITL); FourKites 5 twins + Loft = taksonomia, nie nowa tabela (VISION A.2) |
| W2 | war room + koalescencja N8 | zamknięty HITL katalog ([200.0](deltas/archived/200.0-war-room-mark.md)); leftover N8 / T8 live API / widok sklejony | drugi czat |
| W3 | memory graph na `entity_event` | 201.0 HITL `memory_edge` [delta](deltas/archived/201.0-memory-edge.md); leftover graf / pgvector / FK zdarzeń | RAG na stawkach / umowach CI |
| W4 | Executive AI = narracja po SQL | 202.0 HITL `executive_mark` [delta](deltas/archived/202.0-executive-mark.md); leftover zdania SQL / 117.0 | LLM sumuje |
| W5 | procurement ranking + szkic maila | zamknięty HITL katalog ([203.0](deltas/archived/203.0-rank-mark.md)); leftover ranking SQL / N szkiców | auto-award |

### Fala X — portale / mobile (po **S53**)

| ID | Co | Status | Uwagi |
|---|---|---|---|
| X1–X5 | portal klienta/przewoźnika, apka, outbox consumer, OAuth2 | po S53 + T2 | zastępuje ogólnik S55 |
| X6–X9 | ePOD, lejek PDF (piksel tylko zgoda), podkłady, skan OpenCV | X8 bez OSMF CDN | leftover: `quote_engagement` / `quote_view_token` (X7) · `map_basemap` (X8) · `scan_enhance_run` (X9); karta [karty-pol-fala-x.md](analysis/karty-pol-fala-x.md) |
| **WA1** | WhatsApp Cloud API (Meta WABA); send S11; inbound → HITL | po X + N17 | nie scrape; nie bramki cienia |
| **G9** | SMS + WeChat oficjalne API | z WA1 | TO_VERIFY |
| **G17** | LinkedIn: paste URL + schowek; nie InMail live | z G1+O4 | nie scrape |

### Fala Plat — platforma / Demo-1 / Mob

Karta: [karty-pol-fala-plat.md](analysis/karty-pol-fala-plat.md). R1 (responsive) = DoD od pierwszego UI po P0.

| ID | Co | Status | Poza |
|---|---|---|---|
| Plat-R1 | 360–1920+; tabela→karty | DoD UI | |
| Plat-Env | prod / stage=klon / sandbox API / demo | przed płatnym tenancie | mieszanie danych |
| Admin-P | limity, billing, `platform_usage_daily`; CI = tylko `contracts_count` | | unwrap umów; impersonate≠decrypt |
| Plat-DR | PITR; RPO≤15 min; RTO≤4 h; restore stage co tydzień | | backup bez restore |
| Plat-Scale | k6 real 10k VU na stage | | copy „15k” bez pomiaru |
| **Demo-1** | 10 mies. + 150 aut `demo_sim`; GPS live 7 dni; wipe `USUN` | pełne po T+V+D+G6 | flota klienta na sali; prawdziwe PDF umów |
| **Plat-HD** | ticket produktu: zgłoszenie błędu programu → analiza agenta → akceptacja właściciela przed naprawą | **480.0** DONE HITL `product_ticket_mark` (report/triage/owner_ok); leftover workflow naprawy · Mob; nie CAPA / `operator_notice` |
| **Mob** | Expo iOS/Android + EAS OTA z Admin-P; **dopisek:** sterowanie całym OmniRoute, w tym akceptacja napraw z **Plat-HD** | po S53+X | park Expo `/noc 20` po **480.0**; nie klon BR6.3 / BR2.3; nie `mobile_client_mark`; nie Expo live teraz; następny buildowalny = **AI9.2** HITL |

### Fala CT — wieża załadowcy / 4PL

Karta: [karty-pol-fala-ct.md](analysis/karty-pol-fala-ct.md). Tenant `shipper` RLS. Nie portal Qargo.

| ID | Co | Status | Poza |
|---|---|---|---|
| CT1 | PO → ASN → shipment (U1); plant/SKU | 276.0–278.0 HITL; 291.0 promote ASN→shipment | auto przy POST asn / qty float / live EDI / U1 masowy |
| CT2 | impact chain; klej CI5 | po V6 | auto „zatrzymaj produkcję” |
| CT3 | OTIF pickup vs delivery vs SKU | 280.0 HITL katalog `otif_mark` | OTIF% / scoring SQL |
| CT4 | routing guide 409 | 279.0–290.0: guide · tryb · 409 ASN/shipment · match kind · label match ASN/shipment | live EDI · auto shipment |
| CT5 | EDI 214/315/856/210 + webhook | TO_VERIFY partner | |
| CT6 | SAP/Oracle adapter jak F9 | 281.0 HITL katalog `sap_connector` | live SOAP / SQL do SAP |
| CT7 | p44 **albo** FourKites **albo** Shippeo | 275.0 HITL `p44`; **294.0** tokeny `fourkites`\|`shippeo` (nie live); leftover live HTTP (TO_VERIFY umowa) | scrape ocean |
| CT8 | AIS + kongestia | TO_VERIFY licencja | |
| CT9 | CO₂ GLEC + `methodology_version` CSRD | z C5 | |
| CT10 | freight audit FV vs `charge` | 283.0 HITL katalog `freight_audit_mark` | SQL vs charge / druga marża |
| CT11 | collaboration 3-way role OpenFGA | 284.0 HITL katalog `collaboration_mark` | wspólny SELECT / tuple per strona |
| CT12 | QMS CAPA/8D | 282.0 HITL katalog `capa_mark` | workflow CAPA |

### Fala CI — umowy / SLA / strata / uratowane (kamień sprzedaży)

Karta: [karty-pol-fala-ci.md](analysis/karty-pol-fala-ci.md). **CI9 przed CI1.** LLM nie liczy kar. Extract M-20 **nie** na umowach.

| ID | Co | Status | Poza |
|---|---|---|---|
| **CI9** | zero-knowledge: ciphertext + KEK tenanta; deny-list AI; test super-admin = bytea | 272.0 nagłówek; 273.0 zamknięty opaque BYTEA (`docs/deltas/archived/273.0-customer-contract-ciphertext.md`) — present/absent, nie szyfr; 274.0 zamknięty znacznik owijki (`docs/deltas/archived/274.0-tenant-contract-kek.md`) — nie klucz; leftover `wrapped_dek` / KMS | klucz Omni-master; Langfuse na PDF |
| CI1 | upload + formularz `sla_clause` (wiele umów × odbiorców) | po X1+CI9 | extract LLM |
| CI2 | FV vs umowa (spend leakage) | 320.0 HITL katalog `spend_mark` (leakage_kind); leftover SQL FV vs charge | druga marża |
| CI3 | operacja czyta klauzulę (409/notice) | 317.0 HITL katalog `clause_notice` (etykieta); leftover egzekucja 409 | auto-kara na FV |
| CI4 | `delay_forecast` wcześniej niż okno | 314.0 HITL katalog (`horizon_hours` + `p_late` Decimal); leftover wróżba punktowa / GPS | wróżba punktowa |
| CI5 | które SLA pęknie + kara SQL; bez klauzuli = „brak danych umowy” | 321.0 HITL katalog `penalty_mark` (breach_kind); leftover kara SQL | auto linia produkcyjna |
| CI6 | strata / koszt naprawy / uratowane | 315.0 `remediation_option`; 316.0 `impact_scenario` (etykieta); leftover repair_cost / expected_save / EBITDA SQL / S11 | float; LLM |
| CI7 | scorecard MAE/kalibracja; sample≥N zanim oferta | 318.0 HITL katalog `calibration_mark` (sample_ready); 322.0 HITL katalog `intervention_outcome` (result_kind); leftover MAE SQL / egzekucja sample≥N / saved SQL | suma nachodzących oszczędności |
| CI8 | playbook naprawczy + S11 | 319.0 HITL katalog `repair_playbook` (stance_kind); leftover auto-send S11 | auto-send do jego klienta |

### Fala G — reszta modułów (nie dubluj T–V)

Karta: [karty-pol-fala-g.md](analysis/karty-pol-fala-g.md). G2 wyżej.

| ID | Co | Klej | Poza |
|---|---|---|---|
| G1 | CRM lead→szansa | 323.0 HITL `crm_lead`; **456.0** HITL `crm_opportunity`; leftover activity/pipeline/dedup/X7 | cold auto-send |
| G3 | LC checklista | 324.0 HITL katalog `lc_checklist` (status_kind); leftover bank/due/U5/I3 | bank live |
| G4 | NCTS T1/T2 szkic | 325.0 HITL katalog `ncts_draft` (transit_kind); leftover plomby/C2/PUESC | teatr PUESC |
| G5 | OOG / lashing / eskort | 326.0 HITL katalog `oog_mark` (escort_kind); leftover wymiary/cert/T1 | |
| G6 | load plan OR (osie, bin) | 327.0 HITL katalog `load_plan_mark` (stance_kind); leftover OR/osie/T2 | LLM-VRP |
| G7 | CMMS + DTC | 328.0 HITL katalog `cmms_mark` (work_kind); leftover work_order/DTC/V5 | kara kierowcy |
| G8 | eIDAS / retencja / legal hold | 329.0 HITL katalog `legal_hold_mark` (hold_kind); leftover eIDAS crypto / wipe / F1 | |
| G10 | multi-company w tenancie | 330.0 HITL katalog `company_mark` (seat_kind); leftover company_id FK / drugi tenant | drugi tenant |
| G11 | bonded / miejsce uznane | 331.0 HITL katalog `bonded_mark` (bond_kind); leftover procedura / WMS | WMS e-com |
| G12 | ICS2/CBAM/EUDR/eFTI | 332.0 HITL katalog `filing_scheme_mark` (scheme_kind); leftover filer/deadline/C7 | „SENT-UE” |
| G13 | EDI parser → draft | 333.0 HITL katalog `edi_map_mark` (map_kind); leftover parser/silent write | silent write |
| G14 | AEO dossier | 334.0 HITL katalog `aeo_dossier_mark` (dossier_kind); leftover zestaw party_document / C8 | |
| G15 | yard / waga / EIR | 335.0 HITL katalog `yard_mark` (yard_kind); leftover live yard / WMS / kg / klej D3+T3 | |
| G16 | SaaS billing Omni | 336.0 HITL katalog `billing_mark` (billing_kind); leftover Stripe / limity / S53 | |
| **EXP7.2** | poll CEIDG/KRS/VIES/biała lista → notice | 337.0 HITL katalog `registry_poll_mark` (poll_kind); leftover scrape / auto notice / M-10 | scrape |

### Fala EXP — silniki i pola, które nie wkleiły się wyżej

Pełna lista: [karty-pol-fala-exp.md](analysis/karty-pol-fala-exp.md). `/noc` po G: kolejne EXP2.x / EXP3.x / EXP4.x / EXP5.x których jeszcze nie ma w T–CI. EXP0 = poprawka przy pierwszej fali obiektu. EXP8 = świadome odrzuty (zostają).

### Fala AI — silniki nad katalogami HITL (podnosi V, W, CT, CI)

Wizja: [VISION.md](VISION.md). Ta fala **nie dokłada katalogów** — dobudowuje warstwę liczącą pod katalogi zamknięte w V/W/CT/CI.
`charge.source_ref` jest w kodzie (plaster 129.0, migracja 072) — **AI0 nie jest następnym plastrem**. Kolejność twarda: AI1 → AI2 → reszta. AI4 i AI8.2 odblokowane Q1–Q3.

Dump CT `03` i TMS `04b` **potwierdzają leftover silników** (jeden `charge`, HITL, solver nie LLM). Skrót FourKites / BY / Kinaxis: VISION A.2. Treść dumpów zostaje w badaniach.

| ID | Co | Status | Uwagi |
|---|---|---|---|
| **AI0** | `charge.source_ref` — pochodzenie kwoty na opłacie | **DONE w kodzie** (129.0 / 072) | nullable stare fixture; obowiązkowe na nowym INSERT (`require_source_ref`) |
| AI1.0 | `suggestion_ledger` — każda podpowiedź: BC, encja, przedział/pewność, wersja modelu i promptu, reakcja człowieka `accept\|modify\|reject` **i na co zmienił** | **DONE w kodzie** (432.0 / 342) | HITL append-only, bez zapisu LLM (HC-04); leftover: outcome zamknięty 433.0 / słowniki / trzy BC; dump `04b`: silniki MQ zostają HITL + ten wiersz; `03` B.4 Five twins = taksonomia, nie nowa tabela |
| AI1.1 | `outcome_ledger` — co się naprawdę stało | **DONE w kodzie** (433.0 / 343) | HITL actual_value Decimal; złączenie / CRPS = leftover AI2; bez FK do suggestion_ledger |
| AI1.2 | `counterfactual_run` — scenariusz, punkt odniesienia, dźwignie, wynik; niemutowalny | **DONE w kodzie** (434.0 / 344 · 453.0 / 358) | HITL etykiety + FK migawki + widok powtórki; leftover: solver liczb · AI4.2; nie klon what_if_mark |
| AI1.3 | `benefit_ledger` — zaoszczędzony czas i pieniądze **z jawną metodą punktu odniesienia** | **DONE w kodzie** (435.0 / 345) | HITL method_label + Decimal; nie druga marża; nie SQL z charge |
| AI1.4 | Słowniki otwarte: `twin_kind`, `data_source`, `autonomy_level`, `suggestion_kind` | 436.0–442.0 DONE | leftover `data_source` (AI5) |
| AI2.0 | CRPS, Brier, MAE **liczone** ze złączenia AI1.0×AI1.1 | po AI1.1 | **443.0 DONE** widok; **446.0 DONE** bez wpisu na `prediction_ledger`; leftover: Brier (brak p) · dump `04b`: Oracle LML 95% interval = metoda, nie CRPS/MAE |
| AI2.1 | champion/challenger + wykrywanie dryfu | po AI2.0 | **444.0 DONE** widok średnich; **445.0 DONE** widok dzienny; leftover: detektor/próg `REJECTED` · auto-champion `REJECTED` · zapis `prediction_ledger` (**446.0**) · V1 |
| AI3.0 | `PATCH` na `extraction_draft` + edycja w interfejsie przed akceptacją | po AI2.0 | **447.0 DONE** PATCH `candidates`; **500.0 DONE** quote/rfp; **501.0 DONE** próg 70%; **504.0 DONE** partial `candidate_indexes`; **505.0 DONE** `hitl_confidence_min`; leftover: live vision (`07`) |
| AI3.1 | wersjonowanie szkicu + `draft_kind` + `bbox` i pewność w JSONB | po AI3.0 | **448.0 DONE** `payload.revision` + `bbox_text`/`confidence_text`; **502.0 DONE** HITL `extraction_prompt_mark`; **503.0 DONE** `payload.history`; **515.0 DONE** undo z historii; leftover: wiring Instructor (`07`) |
| AI3.2 | ścieżka **obraz wprost** jako challenger dla obecnej ścieżki przez tekst | po AI3.1 | **449.0 DONE** `extract_path` text|image etykieta; leftover: live vision · pełny pipeline zdjęcia OpenCV/CLAHE (`07` / X9) · AI3.3 · AI3.4 |
| AI3.3 | własny zbiór golden + bramka wydaniowa na progach | po AI3.2 | **450.0 DONE** pytest vs THC/BAF; **509.0 DONE** ≥500; **510.0 DONE** ≥2000; **511.0 DONE** ≥5000; **513.0 DONE** Instructor×golden stub; leftover: DocLayNet / PubTables-1M / CORD / Kleister (licencje, `07`) · żywy OpenAI w CI · 96,6% `TO_VERIFY`; FUNSD / RVL-CDIP `REJECTED` |
| AI3.4 | ekstrakcja z Excela (dziś tylko PDF) | po AI3.1 | **451.0 DONE** `xlsx_sheet` stdlib; **506.0 DONE** `.xls` xlrd; **507.0 DONE** `sheet_index`; **508.0 DONE** `sheet_name`; **512.0 DONE** openpyxl; **514.0 DONE** formuły bez cache; leftover: live vision |
| AI4.0 | `plan_snapshot` z FK do shipment/trip/resource | po AI1; **Q3=tak** | **452.0 DONE** FK złożone RESTRICT; leftover: AI4.1 · CASCADE `REJECTED` |
| AI4.1 | silnik what-if na `counterfactual_run` | po AI4.0 | **453.0 DONE** FK przebieg→migawka + widok `what_if_replay`; leftover: solver liczb · AI4.2 · JSON dźwigni; analog Kinaxis Maestro / scenariusz = HITL, nie live (`03` B.6) |
| AI4.2 | symulacja kółek **w SQL**, do 500k wariantów | po AI4.1 | **454.0 DONE** widok `circle_sim_pair`; leftover: generator 500k · km · VRP |
| AI5.0 | warstwa ingest danych zewnętrznych + `data_source` z licencją | po AI1.4 | katalog: badania `09` / `10`; **22 dostępy P0** z VISION C.1 = ten katalog, nie 22 plastry; **522.0** DONE HITL `data_source`; **523.0** DONE HITL `ingest_gate_mark`; **526.0** DONE HITL `kpi_definition_mark` (otd\|otif\|custom); leftover: live ingest · wzór KPI egzekucja — AI nie wymyśla wzoru; nie OMNI READINESS ENGINE; nie pasek 72 % |
| AI5.1 | cechy modelu predykcyjnego z danych zewnętrznych | po AI5.0 | podnosi V2/V4; **524.0** DONE HITL `model_feature_mark`; leftover: live train (park) |
| AI6.0 | graf skutku biznesowego: Shipment → Inventory → SKU → Production Line → Customer Order → Revenue → Margin → Cash | po AI5.1 + CI1 | Watch Tower technicznie; **519.0** DONE HITL `impact_node_mark`; **520.0** DONE HITL `impact_edge_mark`; leftover: SQL · EBITDA · CT (park) |
| AI7.0 | Cost Allocation Engine — 12 poziomów, 6 kategorii, 23 klucze → `TRUE CONTRIBUTION MARGIN` | po AI0 | marża zostaje w `margin()`; **516.0** DONE `allocation_key`; **517.0** DONE `cost_category_mark`; **518.0** DONE `allocation_level`; leftover: SQL · TCM · AI7.1 |
| AI7.1 | Cyfrowy CFO — narracja **po** SQL, nigdy zamiast | po AI7.0 | anomalia nie jest dowodem; model nie liczy; **525.0** DONE HITL `cfo_narrative_mark`; leftover: silnik narracji (park) |
| AI8.0 | kaskada stylu Global → Company → Department → User → Customer → Person-to-Person → Context | po AI2.0 | bliźniak osoby = styl i relacja, nigdy ocena wyników; **484.0** DONE HITL `style_cascade_mark`; leftover: AI8.1 fidelity · silnik stylu |
| AI8.1 | `STYLE FIDELITY SCORE`, bramka 85% | po AI8.0 | szkic niebrzmiący jak ten użytkownik nie jest proponowany; **485.0** DONE HITL `style_fidelity_mark` (pass/hold/reject/exempt); leftover: silnik score · auto-bramka |
| AI8.2 | poziomy autonomii 0–5 jako dana per tenant i per klient, domyślnie 1 | po AI9.2; **Q1=tak** | `autonomy_level` HITL (438.0); **483.0** DONE HITL `l3_gate_mark`; **486.0** DONE HITL `quality_descent_mark` (powód zejścia); leftover: silnik auto-zejścia · L3 write park; SOP 1 strona w operator/; nie scoring Pain×Frequency; nie Bertha |
| AI9.0 | etykieta art. 50 przy treści z modelu | równolegle od AI3 | AI Act; **521.0** DONE HITL `article50_mark`; leftover: U-art50 UI |
| AI9.1 | przeciwdziałanie automation bias w interfejsie | równolegle od AI3 | **482.0** DONE HITL `automation_bias_mark`; **487.0** DONE HITL `field_confidence_mark` (pasma ui-04); U-art50 zostaje |
| AI9.2 | rejestr ryzyka + program zgodności | przed AI8.2 | **481.0** DONE HITL `risk_register_mark`; **488.0** DONE HITL `compliance_program_mark`; brama L3 DONE 483.0; U-art50 UI zostaje |

### Fala BR — moduły brakujące (równolegle do AI, nie po niej)

Uzasadnienie: [VISION.md](VISION.md) C.3 (w tym Grupa 8). Nie zależą od substratu AI — zależą od osi wejścia (A.5). Start HHL (Q9): **BR3.0**, **BR6.0**, **BR2.0**.

Dump `03` / `04b`: WMS i BR6.2 evidenced; p44/LSP44 = dwie skóry jeden OpenAPI; solver liczy, nie LLM. Treść zostaje w VISION / badaniach.

| ID | Co | Status | Uwagi |
|---|---|---|---|
| BR1.0 | WMS: przyjęcie, lokalizacja, kompletacja, wydanie, inwentaryzacja | rozstrzygnięte: **w zakresie** | **474.0** DONE HITL `wms_flow_mark`; leftover live WMS HTTP · RFID · qty · lokalizacja bin |
| BR1.1 | RFID i identyfikacja automatyczna | po BR1.0 | **475.0** DONE HITL `rfid_mark`; leftover live RFID · EPC · parowanie bin |
| BR1.2 | zapas jako obiekt finansowy: wycena, wiekowanie, Inventory Release | po BR1.0 | **476.0** DONE HITL `inventory_finance_mark`; leftover wycena/wiekowanie SQL · wartość · FK position/PO · live zastaw |
| BR1.3 | zabezpieczenie na towarze: powiązanie pozycji z finansowaniem | po BR1.2 | **477.0** DONE HITL `inventory_collateral_mark`; leftover FK position/PO · live zastaw |
| BR2.0 | `position_event` — pozycja jako osobny byt | **start HHL** (po leftover V5) | **457.0** DONE HITL `position_event`; leftover: lat/lng · poll |
| BR2.1 | urządzenia telematyczne: cykl życia, parowanie z pojazdem, awarie | po BR2.0 | **458.0** DONE HITL `telematics_device`; leftover: parowanie · poll |
| BR2.2 | zgoda na śledzenie jako dana, per kontrahent i per kierowca | po BR2.0 | **459.0** DONE HITL `tracking_consent`; leftover kolumna DONE **634.0**; leftover FK/egzekucja/live poll/Expo |
| BR2.3 | aplikacja kierowcy: zlecenie, POD, skan, status, tryb offline | po BR2.1 | wzorzec offline: Briefcase Builder |
| BR3.0 | planowanie tras — **solver, nie model językowy** | **start HHL** | **455.0** DONE HITL `route_plan_mark`; leftover: Valhalla · VRP · km |
| BR3.1 | planowanie załadunku: osie, wymiary, kolejność, tunele | po BR3.0 | **464.0** DONE HITL `load_order_mark`; leftover: solver · wymiary Decimal |
| BR3.2 | dyspozytor drobnicy: linie, huby, cutoffy, konsolidacja | po D1/D5 | **463.0** DONE HITL `groupage_dispatcher_mark`; leftover: silnik hubów · konsolidacja |
| BR3.3 | tacho jako **ograniczenie planu**, nie raport po fakcie | po BR3.0 + V7 | **465.0** DONE HITL `tacho_plan_mark`; leftover live DDD · solver godzin; office zostaje |
| BR4.0 | promy: rezerwacja, okna, art. 9 | po T | **466.0** DONE HITL `ferry_booking_mark`; leftover live bilet · solver art. 9; art. 9 zostaje |
| BR4.1 | ładunki ponadnormatywne: zezwolenia, pilotaż, trasa specjalna | po BR3.1 | **467.0** DONE HITL `oog_permit_mark`; leftover wymiary Decimal · live zezwolenie; G5 zostaje |
| BR4.2 | konsolidacja morska LCL: konsole, CFS | po D | **468.0** DONE HITL `lcl_console_mark`; leftover live CFS · CBM; D6 zostaje |
| BR4.3 | NAC i agent nominowany | po I | **469.0** DONE HITL `nac_mark`; leftover live NAC · auto-send; I2/I3 zostają |
| BR4.4 | korytarz Chiny-Europa (Jedwabny Szlak) | po BR3.0 | **470.0** DONE HITL `silk_corridor_mark`; leftover UN/LOCODE · km · live CR Express; 110.0 zostaje |
| BR5.0 | faktoring — integracja z partnerem | po F | **471.0** DONE HITL `factoring_connector`; leftover live SMEO HTTP · workflow F7; F wave zostaje |
| BR5.1 | finansowanie zamówienia (PO Financing) | po BR1.2 + BR5.0 | **472.0** DONE HITL `po_financing_mark`; leftover FK PO · wycena zapasu BR1.2 |
| BR5.2 | giełdy transportowe: wymiana ofert | po S55 | **473.0** DONE rozszerzenie CHECK `exchange_connector`; leftover live HTTP · auto-post · wymiana ofert |
| BR6.0 | CRM ponad leada: okazja, aktywność, etap | **start HHL** | **456.0** DONE HITL `crm_opportunity`; **489.0** DONE HITL `crm_activity`; **490.0** DONE HITL `crm_pipeline_mark`; **495.0** DONE HITL `crm_dedup_mark`; **496.0** DONE HITL `crm_link_mark`; leftover: cold-send park |
| BR6.1 | **korytarz jako obiekt sprzedażowy** | po BR6.0 | **460.0** DONE HITL `sales_lane`; **491.0** DONE para UN/LOCODE; **492.0** DONE `volume_label` tekst; **497.0** DONE HITL `sales_bind_mark`; leftover: HubSpot live park |
| BR6.2 | przetargi korporacyjne po stronie załadowcy | po G2 | **461.0** DONE HITL `shipper_tender_mark`; **493.0** DONE HITL `shipper_round_mark`; **494.0** DONE HITL `shipper_like_mark`; **498.0** DONE HITL `shipper_bind_mark`; **499.0** DONE HITL `shipper_award_mark`; leftover: Alpega live park · auto-award SQL |
| BR6.3 | aplikacja mobilna sprzedaży iOS/Android | po BR6.0 | Expo/RN; web UI się nie przenosi |
| BR6.4 | portale: klienta, przewoźnika, podwykonawcy | po S53 | zbieżne z X1–X5 |
| BR6.5 | marketing: kampanie, atrybucja, lejek | po BR6.0 | **462.0** DONE HITL `campaign_mark`; leftover: atrybucja live; nie `funnel_mark` |
| BR7.0 | sala operacyjna — warstwa działająca | po W2 leftover | **478.0** DONE HITL `ops_room_mark`; leftover N8 · widok sklejony · T8 live; `war_room_mark` zostaje |
| BR7.1 | wpływ na linię produkcyjną — warstwa liczona | po AI6.0 | **479.0** DONE HITL `line_impact_layer_mark`; leftover SQL · EBITDA · plant feed; `line_impact_mark` zostaje |

### Fala K — katalog 71–212

| ID | Co | Status |
|---|---|---|
| **K0** | inwentaryzacja **nazw** z rejestru (ID+nazwa+1 linia; nie dump archiwum) | zamknięty ([400.0](deltas/archived/400.0-k0-inventory.md); [K0-inventory.md](state/K0-inventory.md)) |
| K1…Kn | tylko nazwane i niepokryte | puste ID zostają puste |

Zdublowane listy Fal 2–11 (M-xx): [PLAN-HISTORIA.md](state/PLAN-HISTORIA.md). Status żywy = tabela Fala 1 + katalog M-01…M-70.

### Fala SH-R16 — Rejestr wdrożenia 16 IX (fabryka + park)

**Źródło:** 20 plików `D:\OMNIROUTE-badania` (2026-09-16). **Kanon:** [rejestr-wdrozenia-16-ix.md](ops/rejestr-wdrozenia-16-ix.md). Audyt braków → domknięcie 2026-09-16b (szablony 29/29, false DONE, materialne).

**Nie** zastępuje pinu **2026-09-08c**. `/noc`: najpierw otwarte **SH-R16-*** z CURRENT, potem **527.0+**.

| ID | Co | Tryb | Status | Poza / warunek |
|---|---|---|---|---|
| **SH-R16-0** | Rejestr + PLAN + CURRENT | docs | DONE | nie kod 527.0 |
| **SH-R16-1** | Error-budget fabryki | docs | DONE | nie SLO tenanta |
| **SH-R16-2** | Karta PM-FAC W38 | docs | DONE | nie nowy OS |
| **SH-R16-3** | Szablony — **pełne 29/29** (w tym SIGNAL…HIRE) | docs | DONE 2026-09-16b | wypełniaj przy zdarzeniu |
| **SH-R16-4** | Leftover **UXCL-L1** eventy + privacy | leftover | czeka | L0 privacy; nie scoring |
| **SH-R16-5** | Leftover **AI3-payload** | leftover | czeka | żywy OpenAI CI = park |
| **SH-R16-6** | Audit GH Actions / `pull_request_target` | chore | DONE | — |
| **SH-R16-7** | `factory_ai_spend` w WBR | docs | DONE | CEO wkleja $ |
| **SH-R16-8** | False DONE: PROC kanon + path szablonów; PACK-STOP w ops; SLA 7 dni; enum context budget | docs | DONE 2026-09-16b | agentlint w commicie |
| **SH-R16-9** | Materialne: playbooki/RACI/cooling/CEO budget/Diátaxis | docs | DONE (`ops/fabryka-playbooki-sh.md`) | nie next-ID |
| **SH-R16-10** | Rejestr: uzupełnienie R16 gap + statusy spójne | docs | DONE 2026-09-16b | — |
| **SH-R16-11** | Meta-KPI UXCL Closure ≤14 dni — wiersz w PROC + CLOSURE | docs | DONE 2026-09-16b | egzekucja = po UXCL-L1 |
| **SH-R16-12** | FACTORY-PULSE pierwsze liczby (`gh`) | rytuał P-Y | DONE 2026-09-16 ([pulses/FACTORY-PULSE-2026-W38.md](ops/pulses/FACTORY-PULSE-2026-W38.md)) | `/noc` idle + P-Y |
| **SH-R16-13** | Dependabot 1 paczka / tydzień WIP=1 | rytuał idle | czeka (zakaz auto-PR w `/noc`) | nie auto-PR w nocy |
| **SH-R16-14** | Fire/archiwum skill >4 tyg. | rytuał P-Y | DONE 2026-09-16 ([pulses/SKILLS-PULSE-2026-W38.md](ops/pulses/SKILLS-PULSE-2026-W38.md)) — 0 do fire | friday / IDLE |
| **SH-R16-15** | PARK-RADAR Q3/Q4 2026 | rytuał kwartał | DONE 2026-09-16 Q3 ([pulses/PARK-RADAR-2026-Q3.md](ops/pulses/PARK-RADAR-2026-Q3.md)) | idle ≤30 min |
| **UXCL-L1** | Instrumentacja extract-accept | Plan→plaster | zamknięty ([537.0](deltas/archived/537.0-uxcl-l1-extract-accept.md)) | leftover banner zgody · Job#2 charge |
| **AI3-payload** | Payload / delta AI vs człowiek | Plan→plaster | park→CURRENT | SH-R16-5 |
| **Plat-HD-flow** | Obieg ticket→owner | Plan→plaster | zamknięty HITL wpis ([545.0](deltas/archived/545.0-product-ticket.md); S11 owner [546.0](deltas/archived/546.0-product-ticket-owner-s11.md); leftover Mob · auto-fix · FK mark) | G0+G1 + D2 owner |
| **G0-SH** | Host/IdP/CF | — | park | PREMORT→PRR→LAUNCH |
| **SBOM / attestation / EAA / CRA / hire-human** | GIGANT L2–L3 | — | park | rejestr §1.3 |

REJECT rejestr §1.4 = **nigdy** (nie Q). Indeks rytuałów: [fabryka-playbooki-sh.md](ops/fabryka-playbooki-sh.md).

### Parked (w katalogu, nie w kolejce aktywnej)

| ID | Dlaczego nie teraz | Kiedy |
|---|---|---|
| **M-02** outbox | **DONE 79.0** (`inbound_message_saved`). Konsument leftover | S17+ |
| **Auth0 I1/I2** | Brak tenanta / brak sekretu live | po HITL **270.0**. JWT hello zostaje. Cloudflare Access (B.8) **nie** zastępuje tego wiersza |
| **Live public / Cloudflare** | Brak domeny i originu produkcyjnego; Access ≠ IdP | park; [VISION B.8](VISION.md); leftover S53 Auth0 zostaje; nie Q `/noc` |
| **Watchtower / mapa** | **DONE 94.0 + 124.0** lista + liczniki + lazy placeholder | AIS leftover, nie F9.1 |
| **Portale F10** | Brak IdP | **S55** po **S53** |
| **M-04 SSO** | OpenFGA hello ≠ IdP | Razem z Auth0 **S53** |
| **M-03 reszta** | Żyje `default_currency` | **S8** (numeracja/szablon), nie zamiast Q-E |
| **SH-R16 G0 / SBOM / EAA / CRA / hire** | Rejestr 16 IX §1.3 | [rejestr-wdrozenia-16-ix.md](ops/rejestr-wdrozenia-16-ix.md) |

**WIP=1.** Po plasterze: [docs/ops/post-plaster.md](ops/post-plaster.md), PROGRESS, CURRENT = następne Q, push, **nowa rozmowa**. Nie startuj kolejnego Q przy niepushniętym zakresie.

Kolizja numeru historyczna: WIP **0.15 hasła** ≠ **0.15 T0**.

---

## Katalog wydmuszek M-01…M-70 (status, nie spec)

Nie implementuj z tej tabeli „na zapas”. To mapa, żeby nic nie zginęło. Szczegóły obiektów zostają w archiwum aż **Plan** danej pozycji je wciągnie do `docs/spec/` + `MODULES.md`.

| Arch. | Nazwa | Status żywy |
|---|---|---|
| M-01 | Wielodostępność | DONE fundament |
| M-02 | Niezawodność zdarzeń | DONE fundament 79.0 (`outbox_event`) |
| M-03 | Konfiguracja per organizacja | CZĘŚĆ (`default_currency` + prefiks/szablon; numer oferty od 72.0) |
| M-04 | Uprawnienia i tożsamość | CZĘŚĆ (OpenFGA hello; HITL `idp_connector` 270.0; live SSO parked) |
| M-05 | Geografia | DONE fundament (`port` + `location`/strefy + `terminal`/WPI; `operator_party_id` od 5.0) |
| M-06 | Słownik opłat | DONE jako `charge_code` |
| M-07 | Waluty i czas | DONE katalog 6.0; żywy ID **M-23** `nbp_rate` (nie M-07) |
| M-08 | Towary niebezpieczne | kolejka Q6; żywy ID **M-52** `dangerous_good` (nie M-08) |
| M-09 | Kody towarowe | DONE fundament (5.2 katalog) |
| M-10 | Kontrahenci | DONE fundament (5.0 katalog; lookup = fixture) |
| M-11 | Automatyczne kontakty | DONE fundament (8.0 `resolve_email`) |
| M-12 | Sieci i stowarzyszenia | DONE fundament (9.0 `network`; nie katalog agentów) |
| M-13 | Karta wyników kontrahenta | DONE fundament (10.0 `party_scorecard`; nie SQL-refresh) |
| M-14 | Ocena kredytowa | DONE fundament (14.0 `credit_review`; nie auto-scoring) |
| M-15 | Wirtualny Dyrektor Finansowy | DONE fundament (15.0 + 106.0 FV; LLM nie liczy) |
| M-16 | Procedury operacyjne klienta | DONE fundament (11.0 `customer_sop`; nie generator zadań) |
| M-17 | Stawki statyczne | COVERED (`rate_line`) |
| M-18 | Opłaty portowe warunkowe | DONE fundament (12.0 `port_surcharge`; nie zapis do `charge`) |
| M-19 | Stawki live i kanały | DONE fundament (13.0 `channel_quote`; nie live HTTP) |
| M-20 | Pipeline ekstrakcji | DONE fundament HITL |
| M-21 | Silnik wyceny | DONE 2.0 + 5.1 POL/POD/`party_id` |
| M-22 | Narzuty i marża | COVERED (`charge`) |
| M-23–M-31 | Ofertowanie | Fala 3 |
| M-32–M-34 | Komunikacja | DONE fundament (25.0–27.0, 64.0, 66.0, 78.0 ingest `graph://`); pogłębienie **S4–S18** |
| M-35–M-39 | Zlecenie / EDI | DONE fundament (28.0–32.0) |
| M-40–M-47 | Finanse | DONE fundament (33.0–40.0); pogłębienie **S34–S42** |
| M-48–M-51 | Modały | Fala 7 (M-48–M-51 DONE fundament 41.0–44.0) |
| M-52–M-56 | Compliance | Fala 8 (M-52 7.0 + M-53/M-56 DONE 45.0–46.0; M-55 113.0; M-54 114.0) |
| M-57–M-60 | AI / copilot | Fala 9 (M-57 DONE fundament 47.0) |
| M-61–M-67 | Rynek / portal | Fala 10 |
| M-68–M-70 | Ops / wdrożenie | Fala 11 (M-70 DONE fundament 50.0) |

---

## Anti-cele (odmów) + nie pytaj ponownie

Temporal/Hatchet/outbox na zapas · Infisical · 70 pustych M-xx · k6 50k · OTel-sprint · `just perf` / k6 echo jako DoD · Presidio na każdym endpoincie · żywy OpenAI w gate · `can_*` = member · accept bez HITL · hasła+Auth0 w jednym plasterze · persony `.cursor/agents/` · dump Claude · zmiana starych migracji · Next.js · Astro · pgvector „bo stos” · Mission Control jako produkt · Bertha / CoS tenanta · 40 agentów · OMNI READINESS ENGINE jako BC · Cloudflare AI Gateway jako Q · required checks na Free · twierdzenie że 0.12 = IdP · OCR-teatr · zamknięcie Wave FE na adapter+RTL · „powierzchnia 2026” przed Exit Wave FE · auto credit scoring `natural_person` / JDG · zdejmowanie HITL w D0 · Base UI bez ADR · mapa w initial JS · optimistic na kwocie/`accept` · cztery silniki tabel Fiori · 5,0 na tablicy-odczycie · agent sam sobie stawia 4,4 · „szybkie” przy 0 wierszach `rate_line` · drugi plik `AUDIT_PLAN.md` · `.cursorrules` obok AGENTS.

**Nie pytaj ponownie:** Auth0 I1/I2 (aż user ma tenant), IdP, Infisical, Temporal, Pro, dump, „adapter wystarczy na powierzchnię 2026”, „0.12/0.15 = IdP”, start M-02 bez zdarzeń, kompromis na Exit Wave FE, F9.1 bez żywej nazwy.

**Nie ruszać:** ręczny edit `frontend/src/api/*` (flatten anyOf\|null → cast w wrapperze); fałszywy `refactor_ratio`; persony `.cursor/agents/`.

---

## Definition of Done (merge)

1. Delta zamknięta; testy zaakceptowane — tylko to, co gate **naprawdę** egzekwuje + kryteria delty.
2. `just gate` green (+ integration gdy dotyczy).
3. Łowca duplikatów + review 4-pass (**pomiar**; naprawa w pętli).
4. Pętla [post-plaster.md](ops/post-plaster.md); leftover → [docs-debt.md](ops/docs-debt.md).
5. CURRENT + PROGRESS + `just docs` (README/ARCHITECTURE/PLAN z CURRENT).
6. GROUNDING HCs + ADR-0002 (brak drugiego table engine / AI-slop) + ADR-0003 (tokeny, Money, HITL, tenant).
7. **WIP:** nie startuj kolejnego plastra przy niezacommitowanym / niepushniętym zakresie.

## Skills i start

Obowiązkowe: `nowy-plaster`, `zamknij-plaster`, `lowca-duplikatow` (przed kodem), `migracja-rls`, `openfga-change` (gdy model FGA), `ekstraktor` (granica accept), `pr-review`, `knowledge-retrieve` ≤8 kart.

**Nie:** `module-factory` na 70 BC.

<!-- os-start:start -->
**Teraz:** `/plan-modul` (Etap z CURRENT.md).

```
/plan-modul
```

Kontekst: `@docs/state/CURRENT.md` `@docs/PLAN-REALIZACJA.md` `@GROUNDING.md`

Druga komenda (`/plaster`) tylko gdy CURRENT zmieni Etap.
<!-- os-start:end -->
