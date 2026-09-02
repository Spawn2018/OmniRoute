# Playbook Multitask — OmniRoute

**Data:** 2026-09-02  
**Docelowa lokalizacja w repo:** `docs/ops/multitask-playbook.md`  
**Powiązane:** [nocna-zmiana.md](nocna-zmiana.md) · [post-plaster.md](post-plaster.md) · [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Dwa tryby pracy · [CURRENT.md](../state/CURRENT.md)

**Po co:** Cursor Multitask już jest w UI (kilka sesji równolegle, Cloud Agent na własnym worktree, subagenty w jednej sesji). Bez pisanego kontraktu pierwsza równoległa sesja skończy się rozjazdem `CURRENT.md` vs git. To jest awaria planu powstania aplikacji, nie awaria commita.

**Czego ten dokument nie robi:** nie znosi WIP=1, nie otwiera drugiej kolejki, nie pozwala na dwa plastry produktu na `origin/main` w tym samym czasie.

---

## 1. Tryb Cursor × wolno / zakaz

| Tryb | Wolno | Zakaz | Warunek |
|---|---|---|---|
| **Agent + `/plaster`** | Pełny pionowy plaster; commit; push; edycja CURRENT / PROGRESS / delty / migracji | Druga taka sesja gdziekolwiek | Wyłączność na checkout; czysty git; CURRENT Etap = Agent |
| **Plan + `/plan-modul`** | Delta w `docs/deltas/open/`, spec szkielet, zakres w CURRENT | Kod produktu; druga delta na to samo Q | CURRENT Etap = Plan |
| **Ask / odczyt** (dowolna liczba) | Pytania o spec, architekturę, kod; szukanie duplikatów | Jakikolwiek zapis do drzewa | Zawsze wolno, także obok pisarza |
| **Multitask, druga sesja na TYM SAMYM drzewie** | Tylko Ask / Plan / odczyt | `/plaster`, `/zamknij`, `/noc`, commit, push, edycja plików | Pisarz musi wiedzieć, że ta sesja istnieje |
| **Cloud Agent / worktree, inna gałąź** | Recenzja diffu; karta knowledge; how-to; dopisek threat-model; konkurencyjny PLAN **w innym pliku**; eksperyment UI na gałęzi throwaway; ewaluacja promptu na `synth://` | Drugi `/plaster` tego samego M-xx; równoległa migracja Alembic; edycja `CURRENT.md`, `docs/deltas/open/<to samo Q>`, `agentlint.baseline.json`, `AGENTS.md`, `GROUNDING.md`; merge bez rebase; force-push; `--no-verify` | Osobny worktree **i** osobna gałąź; merge robi człowiek po `just gate` |
| **Subagent w jednej sesji** | `lowca-duplikatow`, explore, Bugbot / security-review read-only | Push; edycja CURRENT; 30 person; chat agent↔agent bez artefaktu | Wewnątrz jednego plastra |
| **`/noc`** | Jedna sesja, pętla `/loop`, sama pushuje delty | **Zero** drugiego agenta piszącego gdziekolwiek; zero Multitask w tle | `scripts/noc-preflight.ps1`; czysty git; `main`; jeden busy w NOC-LIVE |

---

## 2. Trzy pasy

### Pas 1 — Pisarz plastra (zawsze dokładnie jeden)

Trzyma checkout, `main`, `CURRENT.md`, migracje, delty. Jedyny, który commituje i pushuje. Zakres = jedno Q z CURRENT. Kończy kartką `/po-plastrze` i pushem; dopiero potem ktokolwiek zaczyna następne Q.

### Pas 2 — Czytelnik / review (dowolna liczba, zero zapisu)

Ask, przegląd diffu, `lowca-duplikatow`, Bugbot, security-review. Produkuje **komentarze i propozycje**, nie pliki. Znalezisko trafia do pisarza albo do issue, nigdy prosto na dysk.

### Pas 3 — Worktree izolowany (0–2, inna gałąź, inne pliki)

Wolno mu pisać, ale tylko: karty knowledge, how-to, dopiski ops, eksperymenty na gałęzi throwaway, ewaluacje na syntetykach. **Nigdy** pliki z listy kolizyjnej. Merge: człowiek → rebase na świeży `main` → `just gate` → push. Gałąź throwaway ma prawo umrzeć bez merge'a i to jest sukces, nie strata.

**Reguła zbiorcza:** pas 3 nie dotyka pliku, który może dotknąć pas 1 w tym samym tygodniu. Jeśli nie wiadomo — to znaczy, że dotknie.

### Lista kolizyjna (zakaz równoległej edycji, także na worktree)

`docs/state/CURRENT.md` · `docs/PLAN-REALIZACJA.md` · `docs/deltas/open/*` · `alembic/versions/*` · `agentlint.baseline.json` · `AGENTS.md` · `GROUNDING.md` · `.cursor/rules/*`

---

## 3. Checklista przed odpaleniem drugiej sesji

1. Czy `/noc` jest aktywna? **Tak → nie odpalam nic.** Koniec.
2. Czy pas 1 istnieje i wiem, co robi? Nie wiem → sprawdzam `CURRENT.md` i `git status`.
3. Czy druga sesja ma pisać? **Nie → wolno, to pas 2, dowolnie.**
4. Jeśli ma pisać: osobny worktree **i** osobna gałąź? Nie → stop.
5. Czy dotknie czegokolwiek z listy kolizyjnej? Tak → **stop**.
6. Czy jej cel to ten sam numer plastra / to samo Q co pas 1? Tak → **stop**, nawet na worktree.
7. Czy `git status` na drzewie pasa 1 jest czysty? Nie → pas 1 najpierw domyka.
8. Kto scala i kiedy? Jeśli odpowiedź brzmi „agent” → **stop**.

W praktyce większość sesji kończy się na pytaniu 3 i jest wolna od razu.

---

## 4. Spięcie z `/noc` i WIP=1

- **WIP=1 dotyczy plastra produktu, nie liczby okien.** Pięć sesji Ask plus jeden pisarz to nadal WIP=1. Dwa worktree piszące karty knowledge to nadal WIP=1, bo żaden nie realizuje wiersza kolejki.
- **Multitask nie startuje kolejnego Q, gdy CURRENT wskazuje inne.** Kolejka jest jedna: `CURRENT.md` + PLAN § Kolejka. Przepustowość rośnie na osi „review, dokumentacja, wiedza”, nie na osi „więcej plastrów naraz”.
- **`/noc` jest trybem wyłącznym.** Preflight sprawdza czysty git, gałąź `main`, jeden busy w NOC-LIVE. Multitask w trakcie nocy to awaria z definicji, także gdy druga sesja „tylko czyta” — pętla `/loop` pushuje i rano nie da się odtworzyć, kto co widział.
- **Drugi agent może** bezpiecznie: review PR, propozycja leftovera do `docs-debt.md`, karta knowledge, how-to operatora, dopisek do threat-modelu, Ask o spec. Nie może zmienić numeru Q ani otworzyć drugiej delty na to samo Q.

---

## 5. Awaria — rozpoznanie i hamulec

**Awaria to jedno z pięciu:**

1. Dwa HEAD-y na `main`.
2. `CURRENT.md` mówi co innego niż `git log`.
3. Dwie delty `open` na to samo Q.
4. Hash agentlinta w innym commicie niż treść kontraktu.
5. `/noc` plus jakikolwiek piszący Multitask.

**Hamulec, w tej kolejności:**

1. Zatrzymaj wszystkie sesje poza pasem 1.
2. `git status` + `git log --oneline -10` na drzewie pasa 1.
3. Porównaj z `CURRENT.md`.
4. Rozstrzygnij **ręcznie**, która delta jest prawdziwa; drugą zamknij z powodem w `docs-debt.md`.
5. `just gate` przed czymkolwiek innym.
6. Dopiero wtedy wznów.

Nigdy nie naprawiaj awarii kolejnym agentem.
