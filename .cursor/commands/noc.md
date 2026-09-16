---
description: Nocna zmiana — pętla plan+plaster+push do podanej godziny
---

Umowa: `docs/ops/nocna-zmiana.md`. Tablica: `docs/state/CURRENT.md`. Kolejka: `docs/PLAN-REALIZACJA.md` § Kolejka.

**Nie wpisuj tu numeru plastra.** Zawsze czytaj CURRENT. Zignoruj pamięć czatu i stare kartki (4.2, jeden plaster, Cloud/PR, stop po dwóch poprawkach).

## Godzina

- `/noc` bez liczby albo `/noc stop` bez trwającej zmiany: wypisz `Użycie: /noc 7` (albo `/noc 8`) i **stop**.
- `/noc stop` przy trwającej zmianie: wyłącz strażnika, dokończ tylko to, co już rozgrzebane, raport, stop.
- `/noc 7` = pętla do **najbliższego 7:00** czasu polskiego (`Europe/Warsaw`). `/noc 8` = do 8:00. Samo `7` = 07:00, nie 19:00.
- Po godzinie: **nie** startuj kolejnego planu ani plastra. Dokończ rozgrzebane, push, raport.

Zostań w trybie **Agent**. **Nie** przełączaj Cursora na tryb Plan (ekran czeka na kliknięcie). **Nie** wołaj narzędzi pytań do operatora.

**Zakaz fire-and-forget:** nie odpalaj pełnej nocy jako `Task` / subagent `run_in_background: true` i nie kończ tury rodzica. Koordynator + `loop-noc` + pętla = **ta sama sesja Agent**. Warstwa 0 (explore / ping) wolno; drugi pisarz na `main` = nie.

## Start (za każdym razem, zanim cokolwiek planujesz)

1. `powershell -ExecutionPolicy Bypass -File scripts/noc-preflight.ps1`  
   Postgres, OpenFGA, internet, GitHub, czysty git, `main`, `pull --ff-only` gdy origin jest do przodu. Exit ≠ 0 → **stop**, nie pętla. Nie `--no-verify`, nie force-push, nie stash cudzej roboty.
2. Zapisz lokalne bicie serca wg `docs/state/NOC-LIVE.example.md` (żywy plik gitignore, nie commitować): `until` ISO, `status: busy` / `idle`, `last_beat`, opcjonalnie `current_cmd`.
3. Strażnik: skill `/loop` co **15 minut**, nazwa `loop-noc`, **w tej sesji**. Prompt budzika:

   > Czytaj lokalne `docs/state/NOC-LIVE.md` i `docs/state/CURRENT.md`. Jeśli `status: stop` albo po godzinie `until`: raport z `docs/ops/nocna-zmiana.md` § Raport, wyłącz loop, stop. Jeśli `status: busy` i `last_beat` świeższy niż 25 min: nic nie rób (trwa prawdziwa praca). Jeśli `last_beat` starszy niż 25 min (także przy `busy`!) i przed `until`: to sesja martwa — w osobnym shellu ubij osierocone `python`/`git` z repo (nie wiszące komendy Cursor), ustaw `status: idle` + świeży `last_beat`, preflight, **jeden** cykl z CURRENT. Nie odpalaj drugiego agenta równolegle. Nie wołaj kolejnego `Stop-Process` gdy poprzedni shell już wisi.

4. Od razu pierwszy cykl (nie czekaj na pierwszy tik). Preflight już odpalił `factory_cycle --start noc` (retrieve + podłoga). Stosuj wypisane karty. Nie pytaj operatora o karty.

Przed **każdym nowym** cyklem (nie w środku pytest): znowu `scripts/noc-preflight.ps1`. Padł Postgres / OpenFGA / sieć / GitHub / podłoga jakości → próbuj start w skrypcie; jak dalej FAIL → stop i raport.

## Cykl (aż do godziny)

Czytaj CURRENT + kolejkę. Leftover HITL/SQL z **Następny** = praca, nie skip. Park live HTTP = brak testu albo sekretu (fixture wolno). Live M-02 konsument / Auth0 / portale tylko gdy CURRENT wskaże to Q. F9.1 bez żywej nazwy — **pomijaj**.

**Etap: Refaktor** → `/refaktor` (max 3 ruchy, testy bez zmiany asercji, karta post-plaster, `/zamknij`, push). Potem następne Q z PLAN Fali E. Nie `/plan-modul` i nie nowy M-xx.

**Brak delty / Etap Plan / wydmuszka** → procedura `/plan-modul` **w tym Agencie** (nie tryb Plan): opcja rekomendowana (bez etykiety: węższa z kolejki Q). W delcie zdanie „wybrane / odrzucone / dlaczego”. Zero kodu produktu. CURRENT: delta zaakceptowana, wolno `/plaster`. `just docs`. Commit + **push** (`docs(M-xx): delta…`). HITL nie zatwierdzaj. Od razu plaster, jeśli przed godziną.

**Delta jest, wolno plaster** → `/plaster` bez czekania na `akceptuję`: `factory_cycle --start plaster` (już w komendzie), łowca duplikatów, spec z CURRENT, plan plików, od razu `/testy` (czerwone), potem kod, skill `zamknij-plaster` **bez nowej rozmowy**. Naprawiaj do skutku. `just docs`.

### Close → commit → push (twarda kolejność)

1. `python scripts/quality/factory_cycle.py --close` — exit 0. PRZESZŁO / następny cykl tylko przy `gate=success` na SHA; `cancelled` ≠ zielone.
2. Istnieje `docs/_bench/cases/<ID>-*.md` dla plastra z CURRENT; plik **w tym samym commicie** co zamknięcie. Brak bench = **zakaz** `git push`.
3. Commit. Dopiero potem push:
   `powershell -ExecutionPolicy Bypass -File scripts/git-push-main.ps1`
   (nie `git push … 2>&1 | Select-Object` — NativeCommandError + duży stderr wieszają PS/Cursor).
4. Limit wall-clock na gate/push: **20 min**. Po timeoutie: nie dokładaj kolejnych wiszących shelli — ubij drzewo w **nowym** oknie PowerShell (`Stop-Process` poza Cursor), `status: idle`, napraw fail (np. brak bench), jeden push przez `git-push-main.ps1`.
5. Po pushu: CI (`gh run watch` / najnowszy run na `main`); czerwone → napraw + push, do skutku albo do godziny. WIP=1.

Moduł niecały → następny plaster (plan jeśli trzeba, potem kod).  
Moduł domknięty → następny Q z PLAN: plan (rozbicie na plastry) → push → plaster → push.

Po pushu zaktualizuj `last_beat` i `status: idle` w lokalnym biciu serca, potem od razu kolejny cykl jeśli przed godziną. Źródło prawdy = CURRENT + git, nie czat.

## Raport (koniec zmiany)

Język dla laika, bez żargonu. Pięć nagłówków z `docs/ops/nocna-zmiana.md` § Raport. Wyłącz strażnika. Lokalne bicie serca: `status: stop`.

Kanon: GROUNDING, GLOSSARY, Decimal, `charge` = marża, ExtractionService bez rates. Nie cofaj hotfixów CI (HANDOFF). Nie 70 stubów.
