# Dług techniczny — żywy rejestr

Aktualizuj **po każdym plasterze** (pętla `docs/ops/post-plaster.md`). Nie dumpuj audytu od nowa.

Źródło początkowe: audyt Gate/DoD + canvas `post-audit-review` (przegląd, nie lista do kodu).

Kolejność pracy: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Rejestr leftoverów.

**Zrobione w syncu (nie wracać):** nagłówek PLAN nie mówi „0.5 lokalnie”; `just test` pada przy failu unita (bez `|| true`).

- **Audyt gate #79–#88:** siedem czerwonych pushy, dwie przyczyny, zero z nich w kodzie produktu. Sześć runów (#79, #80, #82–#85) padło na `agentlint` — hash `AGENTS.md` i `.cursor/rules/context.mdc` rozjechany z baseline. Jeden (#81) na `check_agent_refs`. Kod plastra 4.0 przeszedł pełny gate dopiero w #86; #86/#87/#88 mają wszystkie kroki `success`, więc nic z tej serii nie zostało niezweryfikowane.
- **Kolejność `gate` maskuje kod (leftover, `justfile` nie w tym audycie):** `docs-check → agent-refs → agentlint` idą przed `check`, `test-unit`, `arch`, frontendem. Pierwszy fail meta ubija przebieg, a kroki po `just gate` w `gate.yml` (`audit`, `promptfoo`, `test-integration`) w ogóle nie startują. Skutek: `lint-imports` zepsuty przez 87c4cf3 (brak `__init__.py` w `services/geography` i `repositories/geography`) wyszedł lokalnie, nie z CI — czerwień #82–#85 pokazywała inny powód niż realna usterka. Naprawa = meta-checki po checkach kodu albo osobny job.
- **agentlint to podpis, nie zabezpieczenie:** każda zmiana `AGENTS.md` / `GROUNDING.md` / `.cursor/rules/*` bez `python scripts/quality/agentlint.py --write` w **tym samym** commicie daje czerwony push. Sześć runów z rzędu, bo poprawki szły w commitach, które znowu ruszały kontrakt.
- **check_agent_refs FIXED:** link względny liczy się teraz wobec katalogu własnego pliku. Wcześniej każda ścieżka szła wobec ROOT plus zgadywanie po samej nazwie w `docs/`, `docs/state/`, `docs/spec/` — poprawny `[…](../deltas/open/4.0-port.md)` z `docs/state/CURRENT.md` był fałszywym alarmem (#81), a `../PLAN-REALIZACJA.md` przechodził tylko przypadkiem. Zgadywanie po nazwie zostaje; zwężenie = osobny slot `refaktor-pass`.
- **Skrypty gate'u poza ruffem:** `just check` lintuje wyłącznie `backend`, więc E501 w `scripts/quality/agentlint.py` i `scripts/quality/sync_os_status.py` żyją w narzędziach, które same pilnują stylu. Rozszerzenie zakresu ruff = osobny plaster, nie hotfix.
- **OS słownik DONE:** kanon `/testy` / `/bramka` / skill `zamknij-plaster`; persony z archiwum tylko w tabeli ADR-0001; lint w `check_agent_refs.py`
- **0.15 DONE:** hasła argon2id + `refresh_token` + rotacja; UUID-login wycięty. RLS isolation = integration CI (lokalnie PG wisiał)
- **D0 DONE:** AGENTS stos dziś vs cel; Infisical wycięty; `.cursorignore` na dump; `AGENTS.ARCHIVE.md`; leftover ≠ DONE. HITL i 13 zasad zostają.
- **0.15 T0 DONE:** `document_base64` max_length 2_666_668 → 422 przed decode
- **0.16 T1 DONE:** rola `omniroute_app` NOBYPASSRLS; `DATABASE_URL` runtime. Integration RLS = CI (lokalnie PG wisiał)
- **0.17 T2 DONE:** WITH CHECK + matryca S1–S6; integration = CI
- **0.18 DONE:** HTTP extract live PG + token A / draft B → 404; integration = CI
- **0.19 A1 DONE:** undeclared `/api/v1` → 403; Swagger/ReDoc off
- **0.20 A2 DONE:** `can_review_extractions` = reviewer; seed first-login = member
- **0.21 T4 DONE:** `hello_token` default false; mint UUID tylko przy fladze
- **0.22 T5 DONE:** JWT iss/aud/jti/ver; TTL 15 min
- **0.23 S1 DONE:** JWT_SECRET z GitHub Encrypted Secrets; literał usunięty z gate.yml
- **0.24 DONE:** `/ready` + `X-Request-ID` + SHA pin Actions + `just audit` (pip-audit projektu, nie echo). Auth0 I1/I2 **odroczone**.
- **2.1–2.2 DONE:** Presidio stub tylko na `InstructorExtractor` + 10 syntetyk `synth://`. Nie Presidio-all, nie 30 PDF klienta, nie żywy OpenAI w gate.
- **2.0 DONE:** `quotation` INSERT…SELECT z bieżącego `rate_line` + RLS + `/quotations`. Nie k6, nie marża, HITL bez zmian. Isolation/integration = CI. p95 50k niewymierzony (N/A, nie teatr).
- **3.0 DONE:** `organization_setting` allowlista `default_currency` + RLS + `/organization-settings`. Nie sekrety, nie Infisical, nie outbox. Isolation = CI. **Następny leftover MODULES z jobem operatora:** brak. M-02 bez zdarzeń.
- **4.0 DONE:** `port` UN/LOCODE per tenant + RLS FORCE + `resolve` (alias/kod) + `/ports`. Nie `location`, nie `terminal`, nie WPI, nie `pg_trgm`. **Pierwszy plaster z realnie zielonym `pytest -m integration` lokalnie** (45/45) — nie „PG wisiał, zostaje CI”.
- **4.0 środowisko:** instalator EDB odrzuca argumenty z winget (exit 1, zero własnego logu) także po elewacji — PG 16 stoi jako klaster przenośny `tools/pg16` + `tools/pgdata` (gitignore), start `pg_ctl`. Toolchain lokalny domknięty: `just` 1.58 w `tools/just`, `lint-imports` i reszta skryptów Pythona oraz `psql`/`pg_ctl` dopisane do PATH użytkownika, `sh` dla `just` z `D:\Git\bin`. **`just gate` przechodzi lokalnie w całości**, `just test-integration` 45/45 bez ustawiania zmiennych (domyślne URL-e z `conftest` trafiają w ten klaster). `scripts/dev-native.ps1` znajdzie teraz `psql` przez `Get-Command`, ale pełnego przebiegu skryptu nie weryfikowano. Dysk `C:` = 0 B wolnego (stan zastany, nie z tego plastra) — dlatego nic nie dokładano do `site-packages`, a `npx` pada ENOSPC.
- **4.0 leftover:** `resolve` dopasowuje dokładnie kod albo alias — nie nazwę wiersza; `pg_trgm` / dopasowanie przybliżone dopiero przy realnej potrzebie (ustalenie z delty). Seed 670k wierszy nie odpalony na żywym źródle — ingest dowiedziony fixture'em i `scripts/seed_ports.py`.
- **4.1 DONE:** `location` + `location_zone_member`, typ `postal_range` (kolacja `"C"`), kolumna generowana `postal_span`, exclusion GiST, RLS FORCE na obu tabelach, `resolve(country, postal)` w Postgresie, `/locations`. Migracja `013` dokłada też `uq_port_org_id` na `port` — 4.0 zostawiło tylko unikat po `unlocode`, więc FK złożone nie miało nośnika. Drugi plaster z realnie zielonym `pytest -m integration` lokalnie (61/61). Nie `terminal`, nie WPI, nie `pg_trgm`, nie geometria.
- **4.1 leftover — DDL w dwóch miejscach (dlaczego nie w tym plasterze):** schemat testowy powstaje z `Base.metadata.create_all`, nie z Alembica, więc typ `postal_range`, kolumna generowana `postal_span`, exclusion i indeks częściowy `uq_location_org_code` są odtwarzane w `backend/tests/conftest.py` (`_apply_postal_zone_ddl`) obok polityk RLS. To ten sam wzorzec, którym repo od 0.3 duplikuje RLS — nie nowy dług, ale rośnie. Naprawa = testy jadące przez `alembic upgrade head` zamiast `create_all`; osobny slot `refaktor-pass`, nie plaster domenowy.
- **4.1 leftover — `kind` bez ścieżki zapisu:** `unlocode` i `address` istnieją w schemacie i w CHECK, ale serwis nie ma metody tworzącej takie wiersze — job operatora z delty to wyłącznie strefy. FK złożone do `port` jest dowiedzione na poziomie bazy (`test_location_may_not_point_at_another_tenant_port`). Metoda serwisowa dopiero, gdy pojawi się ekran, który jej potrzebuje — nie „na przyszłość”.
- **4.1 leftover — klony nagłówka modeli:** `jscpd` wskazuje `models/location.py` przeciw `models/app_user.py` i `models/table_view.py`. To wspólny blok `id` / `organization_id` / FK powtórzony w każdym modelu repo, nie duplikat tej domeny. Miksin = zmiana wszystkich modeli naraz, `refaktor-pass`. Próg 3% nadal spełniony (2,92% total).
- **4.1 leftover — konwencja commita:** commit plastra (`2c4b684`) wyszedł bez stopki `Co-authored-by` z `/zamknij`. Wypchnięty na `main`, więc poprawka wymagałaby force-push — zostaje jak jest, konwencja pilnowana od następnego plastra.
- **4.2 DONE:** `terminal` + WPI na `port`, RLS FORCE, `/terminals`, kolumny WPI na `/ports`, ingest fixture + `scripts/seed_wpi.py`. Nie `operator_party_id`, nie live NGA, nie `kind=terminal` na `location`. `just gate` zielony lokalnie.
- **4.2 leftover — pełny CSV NGA (dlaczego nie w tym plasterze):** ingest dowiedziony fixture'em (`wpi_sample.csv`, PLGDY) i skryptem `scripts/seed_wpi.py`. Pełny `UpdatedPub150.csv` nie w git i nie odpalony na żywym tenancie — ten sam wzorzec co seed 670k UN/LOCODE w 4.0. Operator odpala lokalnie, gdy ma plik.
- **4.2 leftover — `operator_party_id`:** **DONE w 5.0.** Tekst `operator_name` zostaje; FK nullable do `party`.
- **5.0 DONE:** `party` + dzieci, RLS FORCE, `resolve(tax_id)`, lookup fixture, OpenFGA `can_manage_parties`, `/parties`, `terminal.operator_party_id`. Nie Q3, nie silnik wyceny z override.
- **5.0 leftover — żywe GUS/VIES/whitelist (dlaczego nie w tym plasterze):** delta = CI fixture, zero sieci. Piaskownica REGON bez klucza w repo. Żywy HTTP = gdy operator ma konto API, nie „na przyszłość” w 5.0.
- **5.1 DONE:** POL/POD + `party_id` na `quotation`, FK złożone, CHECK kompletności, filtry SQL, `/quotations` z pickerami. Kwota nadal ze stawki. Nie override, nie k6.
- **5.1 leftover — powtórzone pickery POL/POD (dlaczego nie w tym plasterze):** formularz i filtry na `/quotations` powielają `<select>`. `dup` poniżej 3%. Wspólny kontroler = gdy trzeci katalog zacznie ten sam wzorzec, albo slot `refaktor-pass`.
- **5.0 leftover — `quotation.party_id` / POL/POD:** Q3, Plan (`/plan-modul`), nie plaster w tym commicie.
- **5.0 leftover — `party_charge_override` w wycenie:** katalog uzgodnień. `quotations` / `charges` / `rate_lines` nie importują. Marża zostaje w `charge.margin()`.
- **5.0 leftover — M-11 matcher domen / OpenFGA per party:** katalog `party_email_domain` bez matchera maili; `can_manage_parties` = member organizacji, nie tuple na wiersz.
- **5.2 DONE:** `commodity_code` HS/CN + aliasy + `source_ref`, RLS FORCE, `resolve`, OpenFGA `can_manage_commodity_codes`, `/commodity-codes`. Nie podpięcie do wyceny, nie IMDG, nie TARIC.
- **5.2 leftover — bliźniacze kolumny katalogu (dlaczego nie w tym plasterze):** `charge_code` i `commodity_code` nadal powielają accessor `code`/`name`/`aliases`. `just dup` 2,91% po wyodrębnieniu `CatalogCreateForm`, `CatalogLoadedTable` i `catalogCreateBody`. Wspólne kolumny = gdy czwarty katalog skopiuje ten sam blok, albo slot `refaktor-pass`.
- **6.0 DONE:** `nbp_rate` tabela A + `source_ref`, RLS FORCE, `resolve(currency, on_date)`, OpenFGA `can_manage_nbp_rates`, `/nbp-rates`. Nie przeliczenie wyceny, nie live NBP, nie M-07 `rate_line`.
- **6.0 leftover — live NBP / Fala 3 (dlaczego nie w tym plasterze):** ingest w CI = fixture; ręczny wpis = `tenant:manual`. `api.nbp.pl` i przeliczenie `quotation` = Fala 3 „Waluty w ofercie”, nie drugi katalog FX.
- **6.0 leftover — klon nagłówka modelu (dlaczego nie w tym plasterze):** `jscpd` 6 linii `charge.py` przeciw `nbp_rate.py` (blok `id`). Miksin wszystkich modeli = `refaktor-pass`. `just dup` 2,83% po kompaktowym `id` i osobnym formularzu kursu (nie `CatalogCreateForm`).
- **U-catalog-parts:** `components/catalog/catalog-parts.tsx` (nagłówek, banner błędu, notka sesji, formularz resolve, formularz create, załadowana tabela). `/charge-codes` i `/commodity-codes` na wspólnym formularzu. `/nbp-rates` bierze nagłówek/tabelę, ale ma własne pola waluta/data/mid. Pozostałe katalogi (`rate-lines`, `charges`, `quotations`, `organization-settings`) nadal mają własne kopie — przepięcie w slocie `refaktor-pass`, nie w plastrze domenowym.
- **ADR-0003 DONE (dokument):** system UI + makiety `docs/design/`. Implementacja = leftover `U-oklch-dark` … `U-print` **poza Q1**. Nie Base UI. Nie mapa w initial JS.
- **0.24 leftover (dlaczego nie w tym plasterze):** `just audit` nie w lokalnym `just gate` (~80 s + sieć PyPI) — CI woła `just audit`; audit = drzewo pyproject, nie host site-packages (pillow/gitpython); image Dockera bez digestu; OpenFGA nie w `/ready`; k6/vulture nadal echo
- **U-routes-breadth DONE:** standing (Charge 1.0–1.2 mają trasy). Exit Wave FE **nie** claim — nie 70 UI, nie „powierzchnia 2026”
- **U-admin-ref DONE:** pulpit = joby operatora; sidebar/toolbar/⌘K.
- **U-pdf-spans DONE:** viewer PDF + spany HITL; lazy pdf.js. Draft nie trzyma PDF (tylko input_text).
- **U-size-limit-real DONE:** `just perf` = build + gzip initial JS < 250 kB; w `just gate`. k6/vulture/pip-audit nadal echo.
- **U-a11y DONE:** skip-to-main + `:focus-visible` + ścieżka operatora.
- **U-density DONE:** compact + toggle na users / charge-codes / rate-lines / charges / extractions.
- **U-palette-ops DONE:** ⌘K akcje operatora (extract, accept-focus, save-view, clear-session).
- **U-art50 DONE:** label „propozycja AI” na recenzji HITL.
- **1.3 DONE:** accept HITL + `rate_line` (kupno) w jednej transakcji HTTP; `ExtractionService` nie importuje rates.
- **1.2 DONE:** `charge` buy+sell + `margin(buy, sell)` + `/charges`. Nie accept HITL
- **1.3 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał przy `pytest -m integration` (jak 0.16–1.2); `just api-types` nie regen — `rate_line_ids` w wrapperze nieczytane, gate = typecheck; brak MCP Postgres w sesji — nowej tabeli nie było; Wave FE U-* DONE; Auth0 I1/I2 odroczone (brak tenanta)
- **U-routes-breadth:** 1.3 = status + link `/rate-lines` na HITL. Nie Exit Wave FE (U-density…U-admin-ref)
- **1.1 DONE:** `rate_line` immutable + `source_ref` + `/rate-lines`. Nie `charge` / marża
- **1.0 DONE:** `charge_code` katalog + aliasy + RLS + `/charge-codes`. Nie `rate_line` / `charge`
- **0.25 DONE:** Money Decimal + waluta + `<Money/>` na HITL. Bez tabeli charge
- **Exit Wave A:** D0 + T0…0.23. 0.24 DONE (audit w CI, nie w local gate)
- **U-routes-breadth:** 1.2 ma `/charges`. 1.1 ma `/rate-lines`. 1.0 ma `/charge-codes`. Nie Exit Wave FE (U-density…U-admin-ref)
- **1.2 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał przy `pytest -m integration` (jak 0.16–1.1); `just api-types` nie regen — wrapper fetch, gate = typecheck; brak MCP Postgres w sesji — schemat z migracji 008/009
- **1.1 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał przy `pytest -m integration` (jak 0.16–0.18 / 1.0); `just api-types` nie regen — wrapper fetch, gate = typecheck
- **1.0 leftover (dlaczego nie w tym plasterze):** isolation/integration = CI — lokalnie PG wisiał (jak 0.16–0.18); `just api-types` nie regen — wrapper fetch, gate = typecheck
- **1.0 leftover:** aliasy jako `TEXT[]` na wierszu, nie osobna tabela — wystarcza resolve; osobny wiersz aliasu gdy 1.1+ tego wymaga
- **Leftover ≠ DONE:** wiersz w tym pliku / PLAN nie zamyka plastra i nie zastępuje `just gate`
- **OAuth/OIDC:** Auth0 I1/I2 **odroczone** (brak tenanta; nie pytać aż będzie). Sesja = email+hasło+JWT (0.15 + 0.12). 0.12/0.15 **nie** są IdP. Zero kodu Auth0 / placeholder tenanta.
- **0.11 DONE:** HTTP XOR 422 + vitest `extractionCreateBody`
- **0.12 DONE:** JWT HS256 hello (`Authorization: Bearer`); identity z claims; OpenFGA nadal AuthZ
- **0.13 DONE:** split-screen HITL (podgląd `input_text` | recenzja); nie PDF canvas
- **0.14 DONE:** HTTP extract/list/accept/reject (unit + stub `ExtractionService`); `api/extractions.py` ~97%; nie live Postgres
- **0.10 DONE:** langfuse trace (no-op bez kluczy) + `just promptfoo` pytest echo — nie cloud, nie żywy LLM, nie `npx promptfoo eval`
- **Po 0.10 (eval):** `npx promptfoo eval` — lokalnie ENOSPC / playwright peers; 30 cenników = osobna decyzja danych
- **2.1–2.2 leftover (dlaczego nie w tym plasterze):** żywy microsoft-presidio; Presidio na każdym endpoincie (cel HC); 30 PDF klienta w eval (zakaz git); `npx promptfoo eval` / OpenAI w gate
- **0.10+ produkt:** żywy instructor/OpenAI w CI, transformers llm-guard, Presidio-all, promptfoo 30 cenników, langfuse cloud
- **Wizja, nie kod:** outbox, Temporal/Hatchet/OTel jako działające systemy
- **Backlog produktu:** HTTP extract vs live Postgres. PDF canvas HITL = U-pdf-spans (lazy); draft nadal bez blob PDF
- **0.14 leftover (dlaczego nie w tym plasterze):** `api/extractions.py:78` `UnparseableDocument("Brak input_text")` — gałąź obronna po XOR Pydantic (0.11); C901/jscpd na diffie czyste, bez refaktoru testów HTTP
- **Ops:** branch protection UI (GitHub Free private 403) — [branch-protection.md](branch-protection.md); k6 / vulture = echo; `just audit` = pip-audit projektu (0.24); `just perf` = size-limit (U-size-limit-real)
- **Kontrakt FE:** nie edytuj ręcznie `frontend/src/api/*` (flatten anyOf|null → cast w wrapperze)
- **Zakaz:** fałszywe ruchy `refactor_ratio`, folder `.cursor/agents/` z personami, dump `Informacje z claude/` do nowych docs
