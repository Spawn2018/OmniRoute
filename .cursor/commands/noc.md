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

## Start (za każdym razem, zanim cokolwiek planujesz)

1. `powershell -ExecutionPolicy Bypass -File scripts/noc-preflight.ps1`  
   Postgres, OpenFGA, internet, GitHub, czysty git, `main`, `pull --ff-only` gdy origin jest do przodu. Exit ≠ 0 → **stop**, nie pętla. Nie `--no-verify`, nie force-push, nie stash cudzej roboty.
2. Zapisz lokalne bicie serca wg `docs/state/NOC-LIVE.example.md` (żywy plik gitignore, nie commitować): godzina stopu ISO, `status: busy` / `idle`, `last_beat`.
3. Strażnik: skill `/loop` co **15 minut**, nazwa `loop-noc`. Prompt budzika:

   > Czytaj lokalne bicie serca nocy (szablon `docs/state/NOC-LIVE.example.md`) i `docs/state/CURRENT.md`. Jeśli po godzinie stopu: raport z `docs/ops/nocna-zmiana.md` § Raport, wyłącz loop, stop. Jeśli `status: busy` i `last_beat` świeższy niż 25 min: nic nie rób. Jeśli cisza > 25 min i przed godziną: preflight, jeden cykl z CURRENT, bije serce. Nie odpalaj drugiego agenta równolegle.

4. Od razu pierwszy cykl (nie czekaj na pierwszy tik). Preflight już odpalił `factory_cycle --start noc` (retrieve + podłoga). Stosuj wypisane karty. Nie pytaj operatora o karty.

Przed **każdym nowym** cyklem (nie w środku pytest): znowu `scripts/noc-preflight.ps1`. Padł Postgres / OpenFGA / sieć / GitHub / podłoga jakości → próbuj start w skrypcie; jak dalej FAIL → stop i raport.

## Cykl (aż do godziny)

Czytaj CURRENT + kolejkę. Leftover HITL/SQL z **Następny** = praca, nie skip. Park live HTTP = brak testu albo sekretu (fixture wolno). Live M-02 konsument / Auth0 / portale tylko gdy CURRENT wskaże to Q. F9.1 bez żywej nazwy — **pomijaj**.

**Etap: Refaktor** → `/refaktor` (max 3 ruchy, testy bez zmiany asercji, karta post-plaster, `/zamknij`, push). Potem następne Q z PLAN Fali E. Nie `/plan-modul` i nie nowy M-xx.

**Brak delty / Etap Plan / wydmuszka** → procedura `/plan-modul` **w tym Agencie** (nie tryb Plan): opcja rekomendowana (bez etykiety: węższa z kolejki Q). W delcie zdanie „wybrane / odrzucone / dlaczego”. Zero kodu produktu. CURRENT: delta zaakceptowana, wolno `/plaster`. `just docs`. Commit + **push** (`docs(M-xx): delta…`). HITL nie zatwierdzaj. Od razu plaster, jeśli przed godziną.

**Delta jest, wolno plaster** → `/plaster` bez czekania na `akceptuję`: `factory_cycle --start plaster` (już w komendzie), łowca duplikatów, spec z CURRENT, plan plików, od razu `/testy` (czerwone), potem kod, gate, `python scripts/quality/factory_cycle.py --close`, skill `zamknij-plaster` **bez nowej rozmowy**. Naprawiaj do skutku. `just docs`. Commit + **push na origin/main**. Po pushu poczekaj na CI GitHub (`gh run watch` / najnowszy run na `main`); czerwone → napraw + push, do skutku albo do godziny. WIP=1: jeden plaster na raz.

Moduł niecały → następny plaster (plan jeśli trzeba, potem kod).  
Moduł domknięty → następny Q z PLAN: plan (rozbicie na plastry) → push → plaster → push.

Po pushu zaktualizuj `last_beat` i `status: idle` w lokalnym biciu serca, potem od razu kolejny cykl jeśli przed godziną. Źródło prawdy = CURRENT + git, nie czat.

## Raport (koniec zmiany)

Język dla laika, bez żargonu. Pięć nagłówków z `docs/ops/nocna-zmiana.md` § Raport. Wyłącz strażnika. Lokalne bicie serca: `status: stop`.

Kanon: GROUNDING, GLOSSARY, Decimal, `charge` = marża, ExtractionService bez rates. Nie cofaj hotfixów CI (HANDOFF). Nie 70 stubów.
