# OS-1 — fabryka: uczenie i bezpieczne automatyzacje

**Status:** open  
**Data:** 2026-09-02  
**Oś:** fabryka. **Poza osią Q/S.** Nie ma wiersza w `PLAN-REALIZACJA.md`.  
**Śledzenie:** jedna linia w [docs-debt.md](../../ops/docs-debt.md).  
**Okno wykonania:** poza osią Q/S. **Nie startuje zamiast S4.** Nie rebase'ować `0224f1b` (66.0) — commity E1/OS-1 są już rodzicami tego plastra przez kolizję pisarzy 2026-09-02.  
**Docelowa lokalizacja pliku w repo:** `docs/deltas/open/OS-1-fabryka-uczenie-i-automacje.md`

**Zakres:** kontrakt agenta, wiedza fabryki, rytm retro, automacje przypominające, dwa rozjazdy kontraktu.  
**Poza zakresem:** kod produktu OmniRoute; migracje; `frontend/`; zmiana HC; zmiana kolejki Q/S; merge czegokolwiek.

**Wejście, którego autor delty nie miał pod ręką:** `docs/ops/docs-debt.md`, `post-plaster.md`, `nocna-zmiana.md`, `friday-retrospective.md`, `weekly-refactor.md`, `threat-model-tenant-hitl.md`, `.cursor/commands/*`, `.cursor/rules/*`, `.cursor/skills/*`, `.github/workflows/*`, ADR-0002. Twierdzenia o `context.mdc`, `no-slop.mdc`, komendach i `gate.yml` pochodzą z opisu w `claude-briefing-factory.md` §3 i **wymagają potwierdzenia przy wykonaniu**. Twierdzenia oparte na `mcp.json`, `settings.json`, `hooks.json`, `AGENTS.md`, `GROUNDING.md`, `PLAN-REALIZACJA.md`, `CURRENT.md` są twarde.

**Potwierdzenie przy umieszczeniu w repo (2026-09-02):** E1 w `AGENTS.md` + `context.mdc` (`backend/alembic/versions/`). 66.0 S3 jest na `origin/main` *nad* commitami fabryki — nie cofać force-pushem. B12: `docs/_source/` dopisane do `.cursorignore` na `factory-learn`. `/plaster` i skill `nowy-plaster` czytają migracje, nie MCP. E3 = git `pre-commit` (nie auto `--write`). E2 (zebrać oba wyniki `just gate`) nadal bez zgody.

---

## A. Werdykt

To jest dojrzała **taśma**, a nie dojrzały **software house**. Taśma produkuje powtarzalnie. Fabryka nie ma pamięci i nie ma rytmu poza głową operatora.

### Zostaje bez ruchu

| Element | Dlaczego |
|---|---|
| `GROUNDING.md` jako warstwa odmowy nad promptem | Jedyna rzecz wygrywająca z agentem pod presją |
| `AGENTS.md` ≤130 linii, pisany ręcznie | ETH: auto-AGENTS = −3% success, +20% koszt |
| ≤3 alwaysApply + globs + skills on-demand | Budżet tokenów, context rot |
| Hooks jako weto deterministyczne | Nie prośba w prompcie |
| WIP=1 + delta-spec + jedna spec na sesję | Mniej sprzecznych instrukcji niż równoległe agenty |
| `CURRENT.md` = SoT sesji, PLAN § Kolejka = SoT „co dalej” | Jedyne, co trzyma 70 slotów w ryzach |
| `requireApproval` na push/commit/docker/rm/downgrade | `settings.json` — lista dobrze dobrana |
| Rozdzielenie `code-gate` / `meta-gate` na dwa joby CI | Naprawa po runach #79–#88, nie cofać |

### Spina się (kolejność)

1. **Pamięć fabryki.** `docs/_knowledge/` ma ~6 kart; `rules-catalog` i `skills-catalog` puste. Każdy powtórzony błąd CI płacony drugi raz. Sygnał → karta → człowiek merge.
2. **Rytm zamiast pamięci operatora.** Retro istnieje jako plik, nie jako zdarzenie. Automacja przypomina i otwiera issue. Nigdy nie edytuje kontraktu.
3. **Dwa rozjazdy kontraktu** (E1 MCP Postgres, E3 agentlint). Rozjazd jest gorszy niż brak reguły: uczy agenta, że kontrakt bywa nieprawdziwy.
4. **Playbook Multitask** — [docs/ops/multitask-playbook.md](../../ops/multitask-playbook.md).

### Świadomie nie robimy

Żadnego „drugiego mózgu”: zero RAG na repo, zero pgvector, zero Memories na pipeline stawek, zero person. Zero auto-merge, także zielonego. Nie dopinamy MCP Postgres „bo kontrakt tak każe” — tańsza jest korekta kontraktu (E1). Zero drugiej kolejki: ta delta nie ma numeru z osi S.

---

## B. Luki fabryki vs dojrzały SH

| # | Luka | Ryzyko | Bezpieczna zmiana | Zakaz |
|---|---|---|---|---|
| B1 | Knowledge ~6 kart; oba katalogi puste | Ten sam błąd płacony 3×; brak wzorca, więc agent generuje | Człowiek dopisuje kartę ≤80 linii po retro albo po powtórzonym błędzie; retrieve 8–20 | Dump kart; auto-generowanie kart przez LLM; RAG na repo |
| B2 | Cursor Automations = 0 | Retro nie odbywa się w tygodniu, w którym boli | Cron: przypomnienie + issue z checklistą (D1–D4) | Agent merge na `main`; agent edytuje AGENTS/GROUNDING/HC |
| B3 | Brak ewaluacji promptów w taśmie (promptfoo = echo) | Regres ekstrakcji niewidoczny do złego draftu u operatora | promptfoo na `synth://`, ręcznie i w CI na fixture | Żywy OpenAI w gate; PDF klienta w git; ewaluacja na danych tenanta |
| B4 | Kontrakt każe czytać schemat przez MCP Postgres, którego nie ma w `mcp.json` | Agent uczy się, że kontrakt bywa fikcją; albo czyta wszystkie modele na zapas | E1 | MCP z rolą mającą `BYPASSRLS` lub prawo zapisu |
| B5 | Seria #79–#88 na podpisie kontraktu, nie na kodzie | Zmęczenie bramką → nawyk `--no-verify` → realny błąd granic przechodzi (już raz przeszedł) | E3 | Wyłączenie agentlinta; hash w innym commicie niż treść |
| B6 | Bugbot / security-review poza kolejką | Albo nie działają, albo działają i nikt nie czyta | Read-only komentarz na PR; wynik jako wiersz w docs-debt | Bot z prawem commita; bot zdejmujący HITL |
| B7 | Brak playbooka Multitask przy istniejącym UI Multitask | Dwa HEAD-y, dwie delty open na to samo Q, rozjechany CURRENT | `docs/ops/multitask-playbook.md` | Dwa `/plaster`; dwa `/noc`; równoległa migracja Alembic |
| B8 | `/noc` implementuje od razu po czerwonym teście | Mniej HITL w najbardziej autonomicznym trybie; test i kod z jednej głowy | Kartka `/po-plastrze` w pełnej formie także po nocy; rano człowiek czyta diff testów | Pomijanie kartki „bo noc”; zamykanie plastra bez przeczytanego diffu testów |
| B9 | `split-to-prs` vs WIP=1 bez branch protection (Free) | Force-push albo równoległe plastry „bo PR-y” | Zostawić wyłączone aż będzie branch protection UI; do tego czasu pasy z playbooka | Force-push na `main`; równoległe plastry |
| B10 | Golden exemplar wskazany (0.3), ale nienazwany w repo | Agent kopiuje ostatni plik, który widział, nie najlepszy | Nagłówek-komentarz `golden-exemplar:` + mapa w karcie knowledge | Trzydzieści wzorców; wzorzec z tablicy-odczytu |
| B11 | Brak metryki kosztu fabryki | Nie widać, czy zmiany w fabryce pomagają | Dwie liczby w kartce `/po-plastrze`: pushy do zielonego, minuty | Dashboard-teatr; metryka jako cel dla agenta |
| B12 | Nie potwierdzone, czy `.cursorignore` ⊇ `excludePatterns` | Jedna ścieżka archiwum wycieka innym mechanizmem | Test w `meta-gate` porównujący obie listy | Ładowanie archiwum hurtowo pod żadnym pretekstem |

---

## C. Plan uczenia (human-curated)

### C.1 Karty `docs/_knowledge/` — 15 propozycji, ≤80 linii każda

Karta powstaje **po** zdarzeniu, nie przed. Kolumna „kiedy” jest wiążąca.

| # | Ścieżka | Kategoria | Co zawiera | Kiedy |
|---|---|---|---|---|
| 1 | `tools/just-gate-mapa.md` | tools | Który recipe egzekwuje, a który to `echo`; `just meta-gate` ~1 s vs `just gate` ~70 s | pierwsza retro |
| 2 | `tools/agentlint-podpis.md` | tools | Kiedy `--write`, dlaczego w tym samym commicie, jak sprawdzić przed pushem | z E3 |
| 3 | `tools/schemat-bazy-skad.md` | tools | Skąd agent bierze schemat po E1 | z E1 |
| 4 | `tools/migracja-rls-checklist.md` | tools | `organization_id` + `FORCE ROW LEVEL SECURITY` + `WITH CHECK` + test izolacji; rola `omniroute_app` NOBYPASSRLS | najbliższy plaster z tabelą |
| 5 | `tools/openfga-tuple-vs-can.md` | tools | `can_*` ≠ `member`; reviewer ręczny seed; brak relacji = deny | leftover 5.0 albo S53 |
| 6 | `tools/git-worktree-multitask.md` | tools | Trzy pasy w formie poleceń; preflight; jak rozpoznać dwa HEAD-y | po playbooku |
| 7 | `prompts/plan-modul-wejscie.md` | prompts | Minimalny kontekst dla `/plan-modul`; czego nie wciągać | pierwsza retro |
| 8 | `prompts/testy-czerwone.md` | prompts | Czerwony test reguły biznesowej vs test-teatr; dlaczego osobna tura | po pierwszym fałszywym greenie |
| 9 | `prompts/extract-eval-synth.md` | prompts | promptfoo na `synth://`; jak dodać przypadek po realnym błędzie | z B3 |
| 10 | `prompts/post-plaster-kartka.md` | prompts | Pełna tabela, dwie liczby z B11, zakaz autorecenzji noty | pierwsza retro |
| 11 | `memory-patterns/sql-set-based-wycena.md` | memory-patterns | `INSERT…SELECT` z bieżącego `rate_line`; dlaczego nie Python na 50k | druga retro |
| 12 | `memory-patterns/money-decimal-granica.md` | memory-patterns | Decimal w bazie/serwisie, `string` na granicy API i w `<Money/>`; oś integer/fraction/ISO | druga retro |
| 13 | `memory-patterns/hitl-accept-transakcja.md` | memory-patterns | accept → `rate_line` w jednym requeście (1.3); `ExtractionService` nie importuje rates | przed S3 |
| 14 | `memory-patterns/tablica-odczyt-vs-modul.md` | memory-patterns | Trzy pytania: własna tabela? własny zapis? test izolacji? Jeśli nie — nie idzie na 5,0 | **pierwsza retro** |
| 15 | `memory-patterns/hotfixy-ci-nie-cofac.md` | memory-patterns | Pięć hotfixów z PLAN § Gate z jednozdaniowym „dlaczego” | **pierwsza retro** |

**Pierwsza retro tworzy trzy karty: 1, 14, 15.** Reszta po jednej, na zdarzenie. Nie tworzyć wszystkich naraz.

`rules-catalog` i `skills-catalog` **zostają puste**, dopóki nie ma >8 pozycji, których operator nie pamięta z głowy. Katalog pustego katalogu to dług.

### C.2 Golden exemplars

| BC / plaster | Wzorzec czego | Dlaczego ten |
|---|---|---|
| M-01 tenancy (0.3 + 0.16 T1 + 0.17 T2) | Migracja → RLS → `WITH CHECK` → matryca izolacji S1–S6 → rola NOBYPASSRLS | Jedyny BC z izolacją udowodnioną testem |
| M-08 `charge` (1.2) | Jedna tabela = jedna prawda; kupno + sprzedaż + `margin()` | „Nie rozmnażaj tabel pod pojęcie” |
| M-07 `rate_line` (1.1) | Niemutowalność + `source_ref` + `superseded_by` | Provenance; kopiuj przy tabelach faktów |
| M-05 geografia (4.0 → 4.1 → 4.2) | Katalog + seed + `resolve`; trzy plastry zamiast megaplastra | Dzielenie BC na pionowe plastry |
| M-20 extraction HITL (0.18 + 1.3) | Granica AI/zapis: intent → HITL → serwis | HC-04; najczęściej kopiowany przy S3 |
| M-21 quotation (2.0 + 5.1) | Silnik w SQL, nie w Pythonie | HC-07 |

**Anty-exemplar, nazwać jawnie:** dowolna z 27 tablic-odczytów. Wzorzec „trasa + filtr cudzego API” jest w repo najliczniejszy, więc statystycznie agent skopiuje właśnie jego. Karta 14 istnieje po to, żeby to przerwać.

Mechanika: nagłówek-komentarz `golden-exemplar: <czego>` w pliku wzorca + jedna tabela w karcie knowledge mapująca „potrzebujesz X → skopiuj wzorzec Y”. Bez mapy wzorzec jest niewidzialny.

### C.3 Retro spięte z automacją, bez edycji AGENTS

Zasada: **automacja przypomina i otwiera artefakt; człowiek zmienia kontrakt.**

1. Piątek, cron → issue `retro-YYYY-MM-DD` z checklistą (D1). Issue jest artefaktem, nie edycją pliku.
2. Operator ≤30 min: prune alwaysApply, skille nietknięte >4 tyg., karty do dodania, powtórzone błędy CI, leftover który przestał być leftoverem.
3. Wynik rozdziela się na trzy kubły i **nigdy się nie miesza**:
   - karta knowledge → osobny commit, bez agentlinta (knowledge nie jest kontraktem),
   - wiersz w `docs-debt.md` → osobny commit,
   - zmiana kontraktu (`AGENTS.md`, `.cursor/rules`) → osobny commit + `agentlint.py --write` w tym samym commicie.
4. `friday-retrospective.md` zostaje **procedurą**, nie logiem. Log = zamknięte issues. Inaczej plik puchnie i sam staje się rot.
5. Agent nie edytuje `AGENTS.md` / `GROUNDING.md` w wyniku retro. Może zaproponować diff **w komentarzu issue**. Merge robi człowiek.

---

## D. Bezpieczne automatyzacje Cursor (szkice, nie YAML)

Wspólny kontrakt: **żadna nie commituje, nie merguje, nie edytuje HC, nie akceptuje extractu, nie wysyła maila, nie robi bookingu.** Wynik = komentarz, issue albo draft w opisie PR.

### D1 `retro-piatek`

- **Trigger:** cron, piątek rano.
- **Wolno:** otworzyć issue `retro-YYYY-MM-DD` z checklistą; wypisać reguły alwaysApply i ich rozmiar, skille nietknięte >4 tyg., liczbę kart knowledge, listę otwartych delt.
- **Nie wolno:** edytować `.cursor/rules`, `AGENTS.md`, `GROUNDING.md`; zamykać issue; usuwać skilla.
- **HITL:** człowiek zamyka issue; każda zmiana kontraktu to osobny ręczny commit.
- **Sygnał do wyłączenia:** issue zamykane bez czytania trzy tygodnie z rzędu.

### D2 `gate-czerwony-komentarz`

- **Trigger:** `gate.yml` fail na PR albo na push do `main`.
- **Wolno:** komentarz z jedną linią — **który job** (`code-gate` czy `meta`), **który recipe**, pierwsze 20 linii logu; **draft** linii do `docs-debt.md` w treści komentarza.
- **Nie wolno:** commitować do `docs-debt.md`; re-run joba; „naprawiać” kod; zmieniać baseline agentlinta.
- **HITL:** operator kopiuje linię ręcznie albo ją odrzuca.
- **Po co:** adresuje B5 — rozdziela „padł podpis kontraktu” od „padł kod” w pierwszym zdaniu.

### D3 `jakosc-tygodniowa`

- **Trigger:** cron, poniedziałek.
- **Wolno:** issue z trzema liczbami — jscpd %, `refactor_ratio` (przeniesione/dodane, okno 4 tyg.), coverage; delta vs poprzedni tydzień.
- **Nie wolno:** uruchamiać `/refaktor`; edytować kodu; ustawiać progów; blokować merge.
- **HITL:** operator decyduje, czy to zamienia się w slot `/refaktor` (max 3 ruchy; CP-01: trzecie powtórzenie, nie drugie).
- **Pułapka:** `refactor_ratio` był raz fałszywy (PLAN § „nie ruszać”). Jeśli liczba jest niewiarygodna, issue ma to **napisać**, a nie podać liczbę.

### D4 `kartka-po-plastrze`

- **Trigger:** push do `main` z migracją Alembic albo przeniesienie delty `open/` → `archived/`.
- **Wolno:** sprawdzić, czy doszła linia w `PROGRESS.md` i czy `CURRENT.md` wskazuje następne Q; jeśli nie — komentarz „brak kartki post-plaster”.
- **Nie wolno:** dopisywać `PROGRESS.md` / `CURRENT.md`; stawiać noty 4,4–5.
- **HITL:** operator uzupełnia kartkę albo świadomie ją odrzuca z powodem.
- **Szczególnie dla:** `/noc` (B8) — jedyny tryb, w którym kartka realnie umyka.

### D5 `synth-eval-nightly` (opcjonalna, dopiero po D1–D4)

- **Trigger:** cron nocny, tylko gdy zmienił się prompt ekstrakcji albo fixture `synth://`.
- **Wolno:** promptfoo na syntetykach; tabela wyników jako komentarz/issue.
- **Nie wolno:** żywy OpenAI w gate; dane tenanta; zmiana promptu; zapis do bazy.
- **HITL:** człowiek decyduje o rollbacku promptu.

### Czego nie automatyzujemy

Auto-merge zielonego PR-a. Auto-`/refaktor`. Auto-uzupełnianie `CURRENT.md`. Auto-prune reguł. Bot, który „poprawia” `AGENTS.md` po czerwonym agentlincie — to Auto-AGENTS tylnymi drzwiami.

---

## E. Naprawa rozjazdów kontraktu

### E1 — schemat bazy: kontrakt każe MCP Postgres, którego nie ma

**Fakt:** `.cursor/mcp.json` zawiera wyłącznie serwer `github`. `AGENTS.md` § Nawigacja mówi: „Schemat bazy sprawdzasz przez MCP Postgres”. Briefing §3.11 wskazuje to samo w `context.mdc`. Rozjazd jest więc **w obu plikach kontraktu**, nie tylko w regule.

**Decyzja: poprawiamy kontrakt, nie dopinamy serwera.** Dopięcie MCP to nowa powierzchnia dostępu agenta do bazy i ADR-0001 #4 mówi wprost, żeby nie mnożyć MCP w kontekście.

**Zmiana w `AGENTS.md` (jedna linia, bilans linii zerowy — limit 130 zachowany):**

```
- **Schemat bazy sprawdzasz przez MCP Postgres.** Nie czytaj wszystkich modeli.
+ **Schemat czytasz z `backend/alembic/versions/`** (najnowsza migracja tej tabeli) **i z modeli tego BC.** Nie czytaj wszystkich modeli.
```

**Zmiana w `.cursor/rules/context.mdc`:** to samo zdanie, jeśli występuje. Potwierdzić treść przed edycją.

**Procedura commita (rozstrzygnięcie operatora z 2026-09-02):**

1. Osobny commit, **tylko** te dwa pliki. Zero kodu produktu w tym commicie.
2. `just agentlint --write` w tym samym commicie (podpis pod kontraktem).
3. `just meta-gate` (~1 s) **przed** commitem, nie po pushu.
4. Dopiero potem cokolwiek innego.

**Gdyby kiedyś MCP Postgres:** osobny plaster fabryki; rola `omniroute_ro`, `NOBYPASSRLS`, `GRANT SELECT` wyłącznie na `information_schema` / `pg_catalog`; zero DML; connection string z env — wzorzec `${env:GITHUB_PAT}` z `mcp.json` zachować.

### E2 — kolejność gate: meta przed kodem

**Fakt:** w CI naprawione — `gate` i `meta` to dwa niezależne joby (PLAN § Gate). Leftover dotyczy **lokalnego** `just gate` (~70 s przez `pre-push`), gdzie fail-fast nadal może postawić meta przed kodem.

**Propozycja, nie implementacja:**

1. W `justfile` rozdzielić `gate` na `code-gate` i `meta-gate` — nazwy identyczne jak w CI, jedna terminologia w dwóch miejscach.
2. `gate` = uruchom **oba**, nie przerywaj po pierwszym, zbierz oba wyniki, exit ≠ 0 jeśli którykolwiek padł. Raport w dwóch blokach: `KOD:` / `META:`.
3. `code-gate` **przed** `meta-gate` w kolejności wyświetlania — żeby błąd granic modułów nigdy nie chował się za hashem kontraktu.
4. `just meta-gate` zostaje osobnym wejściem i wchodzi do kartki `/po-plastrze` jako krok przed commitem zmiany kontraktu.

**Warunek akceptacji:** lokalny `gate` i CI dają **ten sam werdykt** na tym samym commicie. Rozjazd = nowy dług, nie usprawnienie.

### E3 — agentlint: jak nie powtórzyć serii #79–#88

Anatomia: zmiana kontraktu w commicie A, baseline w commicie B albo wcale → siedem czerwonych pushy → w tym oknie przeszedł niezauważony realny błąd granic modułów. Koszt to nie siedem minut, tylko **jeden przepuszczony błąd**.

1. **Lokalny pre-commit (~10 linii):** jeśli w indeksie jest `AGENTS.md` lub `.cursor/rules/*`, a nie ma `agentlint.baseline.json` → **odmowa commita** z komunikatem „uruchom `just agentlint --write` i dodaj baseline do tego commita”. Weto lokalne jest tańsze niż czerwony push.
2. **Zasada w kartce, nie w AGENTS:** zmiana kontraktu = **osobny commit**, nigdy razem z kodem produktu. Wtedy czerwony agentlint nie ma czego zasłaniać.
3. **Komunikat D2** rozdziela `meta` od `code-gate` w pierwszym zdaniu.

**Nie robimy:** wyłączenia agentlinta; automatycznego `--write` w hooku `afterFileEdit` (bot podpisujący kontrakt = brak podpisu); wyjątku „agentlint nie blokuje na `main`”.

---

## F. Backlog wierszy do PLAN (propozycje, nie kod, nie nowa oś)

Wszystko poniżej to propozycje wierszy albo dopisków do **istniejących** sekcji `PLAN-REALIZACJA.md` § Kolejka lub `docs-debt.md`. Nic nie wchodzi przed 66.0 S3. Zero nowej kolejki.

| Propozycja | Gdzie wpiąć | Warunek startu | Czego to nie jest |
|---|---|---|---|
| How-to operatora per job, wzorzec 62.0 | Leftover przy każdym wierszu S, nie osobny wiersz | Plaster S dotyka trasy operatora | Nie dokumentacja programu; nie `AGENTS.md` |
| Watchtower: mapa jako lazy chunk z własnym budżetem | Dopisek w **S32** | Po S28–S31 | Nie nowy M-xx; nie mapa w initial JS (ADR-0003 §6) |
| Set-based batch dla M-27 | Leftover 20.0 w docs-debt | Gdy p95 realnie boli i są wiersze | Nie k6 na pustej tabeli; nie drugi silnik wyceny |
| KSeF jako osobny plaster | **S35** (istnieje) | Po S34 | Nie w jednym plasterze z M-40 |
| GUS/VIES gdy operator ma klucz | Leftover 5.0 party | Klucz istnieje; CI zostaje na fixture | Nie live w gate; nie scraping |
| NBP HTTP bez `amount * mid` po stronie klienta | Dopisek w wierszach finansowych / leftover 6.0 | — | Nie liczenie kursu poza kodem deterministycznym (HC-02) |
| `pg_trgm` na `port` | Leftover Q1 | Gdy resolve gubi | Nie pgvector |
| OpenFGA tuple per `party` | Leftover 5.0 | Przy S53 albo wcześniej | `can_*` ≠ `member` |
| Rozbicie **S55** na S55a…S55g (M-61…M-67) | Zamiana jednego wiersza na siedem | Po S53 | Nie siedem portali w jednym plasterze |
| `named park` w S21 (kanał live), S33 (EDI), S50 (flota) | Dopisek „parked aż umowa / partner / własne auta” | — | Nie HTTP-teatr bez kontrahenta po drugiej stronie |
| M-203 / M-204 zostają puste | Dopisek w § po S59 | Człowiek nazwie | Nie zgadywanie nazwy |

**Mockup `docs/design/omniroute-briefing-mockup.html`:** użyty wyłącznie jako DNA wizualne. Jest spójny z ADR-0003 tam, gdzie ADR jest jeszcze leftoverem (OKLCH, oś integer/fraction/ISO, `Akceptuj` wyłączony, brak `sum()` w JS) — czyli **wyprzedza kod**. To nie jest dowód, że `U-oklch-dark` albo `U-money-align` są zrobione. Zero wierszy produktu z tego pliku.

---

## G. Nie ruszamy

1. `GROUNDING.md` HC-01…HC-08 — zmiana wyłącznie przez ADR i człowieka.
2. `charge` = jedyna prawda o marży; `rate_line` niemutowalna + `source_ref` + `superseded_by`. Nie drugi silnik pod archiwalne M-17 / M-22 (COVERED).
3. HITL przed zapisem stawki. `ExtractionService` nie importuje rates. Optimistic accept zakazany.
4. LLM nie liczy kwot, marż, VAT, kursów. Decimal, nigdy float. Nie `sum()` w JS.
5. `CURRENT.md` = SoT sesji, PLAN § Kolejka = SoT „co dalej”. Żadnego drugiego planu. Ta delta nie jest wierszem S.
6. Zakaz person w `.cursor/agents/`. Jedyny subagent: `lowca-duplikatow`. Zero chat agent↔agent bez artefaktu.
7. Zakaz dumpu `Informacje z claude/` i `docs/_source/`.
8. WIP=1 na plasterze produktu. Multitask tego nie znosi.
9. Anty-cele z PLAN zostają: Infisical, 70 stubów, pgvector „bo stos”, Next jako app, Temporal/Hatchet na zapas, żywy OpenAI w gate, required checks na Free, `.cursorrules` obok AGENTS.
10. Zakaz scoringu `natural_person` / JDG oraz auto-send / auto-booking / auto-przelew. Na zawsze, nie „do czasu”.
11. Nie cofać pięciu hotfixów CI z PLAN § Gate.
12. Nie zdejmować agentlinta, nie automatyzować podpisu pod kontraktem.

---

## Definicja ukończenia tej delty

1. E1 wykonane osobnym commitem (`AGENTS.md` + `context.mdc` + `agentlint --write`), `just meta-gate` zielony przed commitem.
2. E2 pozostaje **propozycją** (lokalny `just gate` fail-fast). E3 wykonane: git `pre-commit` + `pre_commit_factory.py` — bez auto `--write`.
3. Karty knowledge 006–008 (tools) i 002–003 (memory-patterns) w tym samym oknie co zamek drzewa. Dalsze karty tylko po zdarzeniu.
4. `friday-retrospective.md` potwierdzony jako procedura; jeśli jest logiem — jeden ruch redakcyjny, bez zmian w AGENTS.
5. Automacje D1–D4 opisane w `docs/ops/`; **żadna nie włączona** bez osobnej zgody. D5 nietknięta.
6. Zero kodu produktu. Zero zmian w `PLAN-REALIZACJA.md` (śledzenie tylko przez docs-debt).
7. Kartka `/po-plastrze` nie dotyczy tej delty (to nie plaster produktu) — zamknięcie = linia w docs-debt i przeniesienie do `archived/`.

## Leftover z tej delty (do `docs-debt.md`)

- E2: lokalny `just gate` ma zebrać **oba** wyniki (code + meta), nie przerywać po pierwszym — brak zgody na zmianę `justfile` gate.
- B12: `.cursorignore` ma `docs/_source/`; test `⊇ excludePatterns` w `meta-gate` nadal nie istnieje.
- B3 promptfoo na `synth://` — nadal echo.
- D1/D3/D4 Cursor Automations — szkic w [automations.md](../../ops/automations.md), **nie włączone**.
