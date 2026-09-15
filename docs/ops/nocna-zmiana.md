# Nocna zmiana

Operator odpalasz w Cursorze, tryb Agent: **`/noc 7`** (albo `/noc 8`). To jest pętla do **najbliższej** takiej godziny czasu polskiego. Komenda bez godziny nie startuje. **`/noc stop`** kończy strażnika.

To nie jest drugi plan produktu. Kolejka: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. Tablica: [CURRENT.md](../state/CURRENT.md). Numer plastra **nie** jest wpisany w `/noc` — agent zawsze czyta CURRENT. Po Fali E: **Fala S** (pogłębienia). `/plaster` przy Etap Refaktor = stop (`/refaktor`).

**Dwa foldery.** Gdy ta pętla **chodzi** (`NOC-LIVE` = `busy`): commit/push/CI = OmniRoute + GitHub; nowe notatki = `D:\OMNIROUTE-badania`. **Zakaz** promocji badań do kanonu / skilli / kontraktów w trakcie nocy. Gdy noc **stoi**: produkt zostaje w tym repo; przeniesienie z badań (plan, kanon, agent, kontrakt) **tylko** po jawnym poleceniu operatora. VISION D.8.

## Zanim cokolwiek ruszy

Za każdym włączeniem i przed każdym **nowym** cyklem:

```
powershell -ExecutionPolicy Bypass -File scripts/noc-preflight.ps1
```

Skrypt sprawdza: czysty git, gałąź `main`, internet (GitHub), `git fetch` / `ls-remote`, Postgres `:5432`, OpenFGA `:8080`, potem `factory_cycle --start noc` (retrieve + podłoga jakości). Jeśli baza albo OpenFGA leżą — próbuje je podnieść (`pg_ctl`, `openfga.exe`). FAIL = noc **nie** startuje i nie sprząta cudzego drzewa.

Ty: komputer nie usypia, Cursor otwarty. Drugi `/noc` na `main` = zakaz. Pas pomocniczy: niżej, nie drugi plaster kodu.

## Pętla

1. Czytaj `CURRENT.md`. **Etap: Refaktor** → `/refaktor` (max 3), karta post-plaster, commit i push — nie `/plan-modul`.
2. **Etap: Plan** → `/plan-modul` w Agencie (nie przełączaj na tryb Plan w Cursorze — ten ekran czeka na Ciebie). Opcja rekomendowana. Delta + CURRENT. **Commit i push.** Zero kodu produktu.
3. **`/plaster`** (gdy Etap nie jest Plan ani Refaktor): preflight już zrobił retrieve; **nie** wołaj `--start plaster` (NOC-LIVE ≠ stop). Plan plików bez `akceptuję` → czerwone `/testy` → kod → `/po-plastrze` → **`factory_cycle --close` (exit 0) + bench w tym samym commicie** → zamknięcie. **Commit, potem push** na `origin/main`. Naprawia do skutku. Po pushu czeka na CI GitHub i poprawia, aż zielone albo padnie godzina.
4. Kolejny plaster tego modułu, potem kolejne Q z CURRENT (**oś leftoverów**, nie skip named park HITL) — aż do godziny.
5. Po godzinie: nie zaczyna nowego planu ani plastra. Dokańcza rozgrzebane, puszcza, **raport**.

Planowanie zostaje (delta, zakres, testy zanim kod). Znika tylko czekanie na kliknięcie.

### Close → commit → push

Bez `docs/_bench/cases/<ID>-*.md` dla plastra z CURRENT **zakaz** `git push` (pre-push padnie na `test_live_current_has_a_bench_case`). Kolejność: `factory_cycle.py --close` → commit z benchem → `powershell -File scripts/git-push-main.ps1` (nie `git push 2>&1 | Select-Object`). Gate/push: limit **20 min**; po timeoutie ubij osierocone `python`/`git` w **osobnym** oknie PowerShell, nie dokładaj wiszących shelli w Cursorze. `just test-unit` nie drukuje tabeli coverage w terminalu (próg 80% zostaje).

### Strażnik (`loop-noc`)

Co 15 minut (`/loop`, nazwa `loop-noc`) **w tej samej sesji Agent** co `/noc` — nie fire-and-forget `Task` z czatu-rodzica, który kończy turę.

- `busy` + `last_beat` < 25 min → nic nie rób (pytest/commit żyje).
- `last_beat` > 25 min **także przy `busy`** → sesja martwa: ubij orphan, `idle`, preflight, jeden cykl z CURRENT.
- Szablon: [NOC-LIVE.example.md](../state/NOC-LIVE.example.md). Żywy plik lokalny (gitignore).

## Leftover ≠ skip

`parked` w leftoverze pola HITL, SQL na istniejącej tabeli, PDF/ZPL lokalnie, `consignment`, `stop_group`, `plan_snapshot`, konsument outboxa = **praca**, gdy CURRENT ma to w łańcuchu Następny.

Park **live HTTP**: brak testu / sekretu. Wolno fixture + kształt adaptera. Puste sekrety = 503, nie cichy skip.

M-02 konsument, Auth0, portale — **live** tylko gdy CURRENT **wskazuje ten ID jako bieżące Q**. Nie zgaduj S53 przy cutoffie T3. F9.1 bez żywej nazwy — pomiń.

## Pas pomocniczy (multitask bez drugiego `main`)

Godzina, jeden plaster kodu, jeden `git push` na `origin/main` zostają.

- **Koordynator** = ta sesja `/noc` (nie background-only subagent całego `/noc`): `CURRENT.md`, Alembic, push, raport, `loop-noc`.
- **Warstwa 0:** w tej samej sesji wolno Task `explore`, pingi, `gh run watch`, `/loop`, oraz zapis **w git worktree** tylko `docs/deltas/open/**` po zielonym CI N. Przy `status: busy` zero drugiego zapisu w drzewie `main`.
- **Warstwa 1 (opcjonalny drugi czat):** nie drugi `/noc`. `powershell -File scripts/noc-preflight.ps1 -Helper` z katalogu worktree. `writer_preflight.py --allow-noc-helper`. Nigdy `--allow-noc` na pomocniku. Nigdy `git push origin/main`.
- Merge delty N+1: tylko koordynator, `status: idle`, CI zielone, `git merge --ff-only`. Konflikt = abort.
- Czarna lista (nigdy `claimed`, nigdy merge z worktree): `docs/state/CURRENT.md`, `docs/PLAN-REALIZACJA.md`, `backend/alembic/versions/**`.
- Cloud Agent na `main` = zakaz.

## Twarde stop

- HITL: nic z ekstrakcji LLM do bazy bez Ciebie.
- LLM nie liczy. `charge` = marża. Decimal.
- ExtractionService nie importuje rates.
- Brak `organization_id` / RLS / testu izolacji = nie push.
- Brak bench `docs/_bench/cases/<ID>-*.md` po `factory_cycle --close` = nie push.
- Brudne drzewo, rozjazd z origin, nie-main = preflight FAIL (koordynator).
- Bez `--no-verify` i bez force-push.
- Pełne `/noc` jako fire-and-forget background Task = zakaz.

Zarys modułu: Plan rozbija na plastry i robi gęsty job operatora (ekran + baza + flagi w ustawieniach tam, gdzie da się wyciąć na produkcji). Nie 70 pustych szafek.

## Raport (koniec, język jak dla laika)

1. **Co się udało** — co weszło na główną szynę, bez nazw plików.
2. **Gdzie jesteśmy** — jedno zdanie z tablicy.
3. **Ile jeszcze przed nami** — następne duże tematy z kolejki (nie numery M-xx); live bez sekretu nazwij „odłożone HTTP”.
4. **Problemy i jak je załatwiono** — albo „spokojna zmiana”.
5. **Co warto pochwalić** — jedna–trzy rzeczy, bez laurki na siłę.
