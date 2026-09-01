# Nocna zmiana

Operator odpalasz w Cursorze, tryb Agent: **`/noc 7`** (albo `/noc 8`). To jest pętla do **najbliższej** takiej godziny czasu polskiego. Komenda bez godziny nie startuje. **`/noc stop`** kończy strażnika.

To nie jest drugi plan produktu. Kolejka: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md). Tablica: [CURRENT.md](../state/CURRENT.md). Numer plastra **nie** jest wpisany w `/noc` — agent zawsze czyta CURRENT.

## Zanim cokolwiek ruszy

Za każdym włączeniem i przed każdym **nowym** cyklem:

```
powershell -ExecutionPolicy Bypass -File scripts/noc-preflight.ps1
```

Skrypt sprawdza: czysty git, gałąź `main`, internet (GitHub), `git fetch` / `ls-remote`, Postgres `:5432`, OpenFGA `:8080`. Jeśli baza albo OpenFGA leżą — próbuje je podnieść (`pg_ctl`, `openfga.exe`). FAIL = noc **nie** startuje i nie sprząta cudzego drzewa.

Ty: komputer nie usypia, Cursor otwarty, **żaden inny agent nie pisze**.

## Pętla

1. **`/plan-modul` w Agencie** (nie przełączaj na tryb Plan w Cursorze — ten ekran czeka na Ciebie). Opcja rekomendowana. Delta + CURRENT. **Commit i push.** Zero kodu produktu.
2. **`/plaster`**: plan plików bez `akceptuję` → czerwone `/testy` → kod → zamknięcie. **Commit i push** na `origin/main`. Naprawia do skutku. Po pushu czeka na CI GitHub i poprawia, aż zielone albo padnie godzina.
3. Kolejny plaster tego modułu, potem kolejny moduł z kolejki — aż do godziny.
4. Po godzinie: nie zaczyna nowego planu ani plastra. Dokańcza rozgrzebane, puszcza, **raport**.

Planowanie zostaje (delta, zakres, testy zanim kod). Znika tylko czekanie na kliknięcie.

Strażnik co 15 minut (`/loop`, `loop-noc`): jeśli sesja umarła (brak bicia serca > 25 min) i jest przed godziną — wraca do CURRENT, nie do pamięci czatu. Jeśli właśnie trwa pytest/commit — budzik nic nie robi. Plik `docs/state/NOC-LIVE.md` jest lokalny (gitignore), nie commitować.

## Twarde stop

- HITL: nic z ekstrakcji LLM do bazy bez Ciebie.
- LLM nie liczy. `charge` = marża. Decimal.
- ExtractionService nie importuje rates.
- Brak `organization_id` / RLS / testu izolacji = nie push.
- Brudne drzewo, rozjazd z origin, nie-main = preflight FAIL.
- M-02, Auth0, portale — parked, nie zgaduj.
- Bez `--no-verify` i bez force-push.

Zarys modułu: Plan rozbija na plastry i robi gęsty job operatora (ekran + baza + flagi w ustawieniach tam, gdzie da się wyciąć na produkcji). Nie 70 pustych szafek.

## Raport (koniec, język jak dla laika)

1. **Co się udało** — co weszło na główną szynę, bez nazw plików.
2. **Gdzie jesteśmy** — jedno zdanie z tablicy.
3. **Ile jeszcze przed nami** — następne duże tematy z kolejki (nie numery M-xx); parked nazwij „odłożone”.
4. **Problemy i jak je załatwiono** — albo „spokojna zmiana”.
5. **Co warto pochwalić** — jedna–trzy rzeczy, bez laurki na siłę.
