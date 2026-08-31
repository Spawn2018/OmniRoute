# Rewizja na podstawie badań

Weryfikacja czterech obszarów. Wnioski przekładam na konkretne poprawki
w `AGENTS.md`, kicie konfiguracyjnym, podręczniku i rejestrze modułów.

---

# CZĘŚĆ 1 — CZEGO NIE WYKORZYSTYWAŁEM W CURSORZE

Siedem mechanizmów, których nie było w moich rekomendacjach. Dwa są krytyczne.

## 1.1 Hooks — mechanizm, którego brakowało najbardziej ⚠

<cite index="27-1">Cursor Hooks wprowadzone w 2026 to skrypty podpinane do zdarzeń edytora: `onPreEdit` przed zastosowaniem zmian przez agenta z możliwością weta, `onPostEdit` po zapisie na dysk, `onPreCommit` przed przygotowaniem commita, `onApprove` przy akceptacji diffa. Są to skrypty bash, Node albo Python w katalogu `.cursor/hooks/`. Typowe zastosowania: blokowanie edycji plików produkcyjnych, automatyczne formatowanie każdego pliku, uruchomienie `tsc --noEmit` po każdej edycji i **zwrócenie błędów z powrotem do agenta**.</cite>

To jest bezpośrednia odpowiedź na dane z części 2. Zamiast czekać na CI, agent
dostaje informację zwrotną natychmiast po każdej edycji i sam się poprawia.

<cite index="26-1">Skrypt hooka otrzymuje wejście JSON i zwraca `followup_message`, kontynuując pętlę iteracji — co jest nieocenione dla automatycznych przepływów typu „napraw, testuj, napraw ponownie".</cite>

**Do dodania: `.cursor/hooks/`**

```python
# .cursor/hooks/post_edit.py  — uruchamiany po każdej edycji agenta
import json, subprocess, sys

payload = json.load(sys.stdin)
path = payload["file_path"]
problems = []

if path.endswith(".py"):
    subprocess.run(["ruff", "format", path], check=False)
    r = subprocess.run(["ruff", "check", "--select",
                        "E,F,B,C901,ARG,PLW0621,SLF001", path],
                       capture_output=True, text=True)
    if r.returncode:
        problems.append(r.stdout)
    m = subprocess.run(["mypy", path], capture_output=True, text=True)
    if m.returncode:
        problems.append(m.stdout)

elif path.endswith((".ts", ".tsx")):
    t = subprocess.run(["pnpm", "tsc", "--noEmit"],
                       capture_output=True, text=True)
    if t.returncode:
        problems.append(t.stdout)

if problems:
    print(json.dumps({
        "followup_message":
            "Popraw poniższe zanim przejdziesz dalej:\n" + "\n".join(problems)
    }))
```

Reguły `ruff`, które wybrałem, nie są przypadkowe — odpowiadają pięciu
najczęstszym błędom agentów udokumentowanym w części 2: `B` (broad except),
`F401/F841` (nieużywane), `ARG` (nieużywane argumenty), `PLW0621` (przesłonięte
zmienne), `SLF001` (dostęp do składowych chronionych).

**`.cursor/hooks/pre_commit.py`** — blokuje commit przy naruszeniu architektury:

```python
checks = [
    ["lint-imports"],
    ["jscpd", "--threshold", "3", "--reporters", "console", "backend/app"],
    ["vulture", "app", "--min-confidence", "80"],
]
```

**`.cursor/hooks/pre_edit.py`** — weto na plikach, których agent nie ma ruszać:
migracje już zastosowane, katalog `frontend/src/api/` (generowany), `docs/adr/`
ze statusem „przyjęta".

## 1.2 Skills — oszczędność kontekstu, której nie stosowałem

<cite index="29-1">Skills definiuje się w plikach `SKILL.md` i mogą zawierać komendy własne uruchamiane przez `/`, hooki oraz wiedzę domenową. W odróżnieniu od Rules, które są zawsze dołączane, Skills ładują się dynamicznie, gdy agent uzna je za istotne — co utrzymuje okno kontekstu czyste, dając jednocześnie dostęp do wyspecjalizowanych możliwości.</cite>

Wszystko wrzuciłem do Rules. Część powinna być Skills — ładowana wtedy, gdy
agent jej potrzebuje, a nie zawsze.

**Podział, który proponuję:**

| Warstwa | Zawartość | Kiedy w kontekście |
|---|---|---|
| `AGENTS.md` | 13 zasad, nawigacja, budżety | zawsze |
| Rules z `globs` | konwencje per katalog | przy dotknięciu plików |
| **Skills** | procedury domenowe | gdy agent uzna za istotne |

**Skills do utworzenia** (`.cursor/skills/`):

- `nowy-modul/SKILL.md` — pełna procedura pionowego plastra
- `migracja-rls/SKILL.md` — jak dodać tabelę z RLS i testem izolacji
- `adapter-armatora/SKILL.md` — jak dodać kanał do M-19
- `workflow-temporal/SKILL.md` — wzorzec workflow z sygnałami
- `ekstraktor/SKILL.md` — jak dodać parser do pipeline M-20
- `komponent-tabeli/SKILL.md` — TanStack Table z wirtualizacją i Money
- `debug-wydajnosci/SKILL.md` — EXPLAIN → py-spy → poprawka

## 1.3 Subagenty

<cite index="34-1">Wydanie ze stycznia 2026 wprowadziło subagenty — niezależne agenty działające równolegle z głównym, każdy z własnym oknem kontekstu i narzędziami. Przykład zastosowania: podczas gdy omawiasz architekturę z głównym agentem, jeden subagent uruchamia testy, drugi pisze dokumentację, trzeci bada dobre praktyki.</cite>

Zastosowanie u ciebie: podczas implementacji plastra subagent aktualizuje
`docs/spec/`, drugi uruchamia zestaw testów wydajnościowych. Nie zaśmiecają
kontekstu głównego.

## 1.4 Pozostałe trzy

**Plan Mode z katalogiem `.cursor/plans/`** — plany zapisywane jako pliki,
nie ginące w rozmowie. Wersjonowane w gicie.

**Komendy własne** uruchamiane przez `/` — `/plaster`, `/bramka`, `/refaktor`
zamiast przeklejania tych samych promptów.

**Import reguł z repozytorium GitHub** — <cite index="28-1">Cursor pozwala importować reguły bezpośrednio z dowolnego repozytorium GitHub, publicznego lub prywatnego, skanując wszystkie pliki `.mdc`.</cite> Twoje reguły trzymasz w osobnym repo i współdzielisz między projektami.

**Kolejność reguł:** <cite index="28-1">Team Rules → Project Rules → User Rules, wszystkie scalane, przy konflikcie wygrywa wcześniejsze źródło.</cite>

---

# CZĘŚĆ 2 — DANE EMPIRYCZNE O DŁUGU Z KODU AI

To jest najważniejsza część tej rewizji. Liczby są jednoznaczne i zmieniają
priorytety.

## 2.1 Co pokazują badania

**GitClear, 600 mln commitów, dane do 2026:**

<cite index="40-1">Duplikacja bloków kodu rosła w każdym roku okresu badania. Mierzona na milion zmienionych linii, wzrosła z 40,3 w 2023 do 73,0 w 2026 — o 81% względem 2023 i najwięcej w historii pomiarów. Odsetek kodu przenoszonego (czyli refaktoryzowanego) spadł z 21% w 2022 do 13% w 2023, a następnie załamał się do 3,8% w 2026. W tym samym czasie kopiuj-wklej wzrósł z 9,4% do 15,7%. W starciu „powielić kontra zrefaktoryzować" programiści są dziś około pięciokrotnie bardziej skłonni do powielenia.</cite>

<cite index="40-1">Obserwujemy wzrost kopiuj-wklej w obrębie commita o 41%, duplikacji bloków o 81%, konstrukcji maskujących błędy o 47% i dwutygodniowego churnu o 15%.</cite>

**MSR 2026, 302 579 commitów autorstwa AI, 6 299 repozytoriów:**

<cite index="38-1">Zidentyfikowano 484 366 odrębnych problemów. Pięć najczęstszych zapachów kodu to: szerokie przechwytywanie wyjątków (41 374 przypadki), nieużywane zmienne (28 272), nieużywane argumenty (24 357), przesłonięte zmienne zewnętrzne (20 647) i naruszenia dostępu do składowych chronionych (19 796). Dług nie leczy się sam.</cite>

<cite index="42-1">Ponad 15% wszystkich commitów wspomaganych AI wprowadza co najmniej jeden problem. Spośród 484 366 problemów 22,7% przetrwało do najnowszych rewizji repozytorium.</cite>

**Najgroźniejsze ustalenie — przegląd nie działa:**

<cite index="41-1">Agenty AI produkują więcej redundantnego kodu (klonów typu 4) niż ludzie. Recenzenci jednak tego nie karzą — przeciwnie, wykazują mniej negatywnego nastawienia wobec pull requestów generowanych przez AI. Powierzchowna wiarygodność kodu AI potrafi maskować złe decyzje projektowe, co prowadzi do ukrytego długu technicznego, w którym redundancja narasta niezauważona.</cite>

<cite index="38-1">Agenty naprawiają mniej więcej tyle samo zapachów, ile wprowadzają, ale konsekwentnie tworzą nowy dług poprawnościowy i bezpieczeństwa, którego recenzenci systematycznie nie wychwytują. Obroną nie jest ograniczanie użycia AI, tylko jego oprzyrządowanie.</cite>

**I ustalenie o produktywności, które warto znać:**

<cite index="36-1">Stwierdzono lukę 39–44% między postrzeganą a rzeczywistą produktywnością doświadczonych programistów pracujących w dojrzałych, złożonych bazach kodu. Programiści czuli się około 20% szybsi, a zmierzony czas realizacji zadań był o 19% dłuższy niż bez wsparcia AI.</cite>

<cite index="36-1">Zespoły osiągające najlepsze wyniki dzielą trzy praktyki: śledzą kod generowany przez AI osobno, ze specjalizowanymi bramkami jakości, oraz mierzą jakość i szybkość razem, a nie wolumen wyjścia.</cite>

## 2.2 Przełożenie na konkretne bramki

| Zjawisko | Liczba | Mechanizm obrony |
|---|---|---|
| Duplikacja bloków | +81%, 73/M linii | `jscpd` próg 3%, hook `pre_commit` |
| Kopiuj-wklej w commicie | 15,7% | `jscpd --min-lines 5` w hooku po edycji |
| **Refaktoryzacja w zaniku** | **21% → 3,8%** | **metryka „moved vs added" w PR** |
| Maskowanie błędów | +47% | `ruff B902,BLE001` w hooku, blokada |
| Nieużywane zmienne i argumenty | 52 629 przypadków | `ruff F841,ARG` w hooku |
| Przesłonięte zmienne | 20 647 | `ruff PLW0621` w hooku |
| Dostęp do składowych chronionych | 19 796 | `ruff SLF001` w hooku |
| Dryf złożoności | — | próg delty: +3 na funkcję w PR = blokada |
| Recenzent nie wychwytuje | udokumentowane | BugBot + `pr-agent` + lista kontrolna |
| 22,7% długu przetrwa | udokumentowane | tygodniowy raport trendu, nie jednorazowy |

**Najważniejsza pojedyncza metryka: stosunek kodu przeniesionego do dodanego.**
Spadek z 21% do 3,8% oznacza, że kod przestał być refaktoryzowany, tylko
dokładany. Jeśli w twoim repozytorium ten wskaźnik będzie niski, wiesz o
problemie zanim stanie się nieodwracalny.

```bash
# scripts/refactor_ratio.py — do raportu tygodniowego
# moved_lines / (added_lines + moved_lines) z git log --numstat
# próg alarmowy: < 10%
```

## 2.3 Śledzenie kodu AI osobno

Wynika wprost z badania LinearB. Praktycznie:

```
# .gitmessage — szablon commita
Co-authored-by: Cursor Agent <agent@cursor.sh>
```

Plus `git notes` z identyfikatorem plastra. Wtedy raport potrafi porównać
gęstość defektów w kodzie pisanym z agentem i bez.

---

# CZĘŚĆ 3 — WYBÓR METODYKI

## 3.1 Scrum odpada i wiem dlaczego

<cite index="49-1">AI zmienia znaczenie punktów historyjkowych. Jeśli narzędzie generuje w dwie godziny funkcję, która zajmowała dwa dni, historyczne dane o prędkości tracą sens. Zespoły w 2026 aktywnie przeliczają sposób szacowania i mierzenia zdolności produkcyjnej. To wciąż problem nierozwiązany.</cite>

Do tego Scrum rozwiązuje problem koordynacji ludzi. Ty jesteś jedną osobą.
Ceremonie, role i sprinty to czysty narzut.

## 3.2 Czego nie robić w drugą stronę

<cite index="44-1">Development sterowany specyfikacją pasuje do funkcji wielosesyjnych i wieloagentowych, zespołów potrzebujących intencji do przeglądu przez interesariuszy, zmian w istniejącym kodzie, gdzie liczy się kontrakt, oraz pracy zbliżonej do compliance. Nie pasuje do: poprawek błędów, prototypów eksploracyjnych i szybkiej iteracji w pojedynkę — tam wygrywa tryb planowania plus dobre testy.</cite>

Czyli maksymalistyczne podejścia z kilkunastoma personami agentów byłyby dla
ciebie narzutem. Ale specyfikacja jako taka jest niezbędna:

<cite index="45-1">Dane empiryczne dokumentują trzy- do pięciokrotny wzrost prędkości u zespołów wdrażających kodowanie wspomagane AI; w tym samym badaniu słaba dyscyplina wymagań wiąże się z wyższym długiem technicznym — złożonością cyklomatyczną, duplikacją kodu i degradacją pokrycia testami — podczas gdy rygorystyczna dokumentacja wymagań wiąże się ze znacznie mniejszymi kompromisami jakościowymi.</cite>

<cite index="50-1">Development sterowany specyfikacją nie zastępuje Agile, Scruma ani DevOps. Jest warstwą pod nimi. Starsze metodyki koordynują ludzi wykonujących pracę; SDD definiuje, przeciwko czemu agent buduje i jak weryfikujesz, że skończył.</cite>

## 3.3 Rekomendacja: przepływ z warstwą specyfikacji i praktykami XP

**Trzy elementy, żadnych ceremonii:**

**① Kanban z limitem prac w toku równym jeden.** Jeden plaster naraz, do końca.
Bez sprintów, bez punktów, bez estymacji. Tablica: `Do zrobienia → Plan →
Testy → Implementacja → Bramka → Gotowe`.

**② Delta-spec zamiast pełnej specyfikacji.** Dokumentujesz zmianę, nie cały
moduł. Cykl: **zaproponuj → zastosuj → zarchiwizuj**, gdzie archiwizacja scala
deltę do `docs/spec/<moduł>.md`. To jest lekkie podejście, które w praktycznych
porównaniach wypadło najlepiej przy pracy iteracyjnej.

```
docs/
├── spec/<moduł>.md          ← źródło prawdy, aktualne
└── deltas/
    ├── open/2.4-silnik-wyceny.md
    └── archived/2.3-oplaty-portowe.md
```

**③ Praktyki XP, bo to one dotyczą jakości.** TDD, ciągła integracja,
refaktoryzacja jako część pracy, prostota. <cite index="49-1">XP idzie głęboko w praktyki inżynierskie: programowanie w parach, TDD, ciągłą integrację i refaktoryzację kodu. Jeśli jakość kodu jest priorytetem, wiele zespołów nakłada praktyki XP na Scruma i osiąga dobre wyniki.</cite>

Programowanie w parach masz w formie zmienionej: **agent jest partnerem, ty
prowadzisz.** To jest dokładnie relacja z pary — jeden pisze, drugi myśli o
kierunku.

## 3.4 Rytm tygodniowy zamiast sprintów

| Kiedy | Co | Czas |
|---|---|---|
| Poniedziałek rano | Wybór plastrów na tydzień, aktualizacja `CURRENT.md` | 30 min |
| Codziennie | Pętla plastra, jeden na raz | — |
| Piątek | **Raport metryk**: duplikacja, złożoność, stosunek refaktoryzacji, budżety | 30 min |
| Piątek | Retrospektywa jednoosobowa: co spowolniło, co poprawić w regułach | 15 min |
| Co 4 tygodnie | Slot refaktoryzacyjny — jeden dzień, wejście z metryk | 1 dzień |

Retrospektywa ma konkretny efekt: **poprawka w regułach albo w hookach**.
Jeśli agent trzy razy popełnił ten sam błąd, to jest brak reguły, nie jego wina.

---

# CZĘŚĆ 4 — POPRAWKI DO DOKUMENTÓW

## 4.1 `AGENTS.md` — dodaj

**Zasada 14 (nowa, wynika wprost z danych):**
> 14. Zanim napiszesz nową funkcję, sprawdź, czy istnieje. Duplikacja jest
>     najczęstszym błędem agentów — trzykrotnie częstszym niż refaktoryzacja.

**Zakazy rozszerzone o pięć udokumentowanych zapachów:**
> - `except Exception` bez konkretnego typu i obsługi
> - nieużywane zmienne i argumenty — usuń, nie komentuj
> - przesłanianie zmiennych z zakresu zewnętrznego
> - dostęp do składowych chronionych spoza klasy
> - kopiowanie bloku powyżej 5 linii zamiast wyodrębnienia

**Sekcja o mierzeniu:**
> Po każdym plastrze hook `pre_commit` sprawdza duplikację, złożoność i martwy
> kod. Naruszenie blokuje commit, nie generuje ostrzeżenia.

## 4.2 Kit konfiguracyjny — dodaj

- katalog `.cursor/hooks/` z trzema skryptami (§1.1)
- katalog `.cursor/skills/` z siedmioma umiejętnościami (§1.2)
- katalog `.cursor/plans/` — plany wersjonowane
- komendy własne: `/plaster`, `/bramka`, `/refaktor`, `/delta`
- rozszerzone reguły `ruff`: `B,BLE,ARG,PLW0621,SLF001,C901,F841`
- `jscpd` z progiem 3% w hooku, nie tylko w CI
- skrypt `scripts/refactor_ratio.py`
- szablon commita z atrybucją agenta
- BugBot włączony na repozytorium

## 4.3 Podręcznik pracy — zmień

**Pętla plastra rozszerzona o hooki.** Krok „bramka" przestaje być osobny —
hook po edycji zwraca błędy agentowi natychmiast, więc do `just gate`
dochodzisz z kodem już czystym stylistycznie.

**Krok zero: delta-spec.** Przed planem piszesz `docs/deltas/open/<id>.md`
z opisem zmiany i kryteriami akceptacji. To jest piętnaście minut, które
badania wiążą ze znacząco mniejszym długiem.

**Dodaj sekcję o weryfikacji.** Podatek weryfikacyjny jest realny —
oszczędzony czas pisania przechodzi na sprawdzanie kodu, który wygląda
wiarygodnie. Planuj go, nie udawaj, że go nie ma.

**Zmień sekcję o przeglądzie.** Skoro badania pokazują, że recenzenci są
łagodniejsi wobec kodu AI, potrzebna jest lista kontrolna, nie wyczucie:

```
Przegląd PR — lista kontrolna
□ Czy ta logika już gdzieś istnieje? (szukaj przed akceptacją)
□ Czy nowa funkcja mogła być rozszerzeniem istniejącej?
□ Czy obsługa błędów jest konkretna, czy maskująca?
□ Czy złożoność którejś funkcji wzrosła o więcej niż 3?
□ Czy testy sprawdzają regułę biznesową, czy implementację?
□ Czy da się to napisać krócej?
```

## 4.4 Rejestr modułów — dodaj

**M-71 · Metryki jakości kodu** (moduł wewnętrzny, nie produktowy)

| Obiekty | Funkcje |
|---|---|
| skrypty w `scripts/quality/` · raport tygodniowy | stosunek refaktoryzacji · duplikacja · trend złożoności · przeżywalność problemów · gęstość defektów w kodzie agentowym vs własnym |

**Repozytoria:** `jscpd` · `vulture` · `knip` · `ruff` · `gitclear`-podobne
liczenie z `git log --numstat`

To jest moduł, który buduje się w dniu pierwszym i działa przez cały projekt.

---

# CZĘŚĆ 5 — TRZY WNIOSKI, KTÓRE ZMIENIAJĄ NAJWIĘCEJ

**① Hooki zamiast nadziei.** Największa różnica między moimi wcześniejszymi
rekomendacjami a stanem wiedzy. Agent poprawiający się po każdej edycji na
podstawie wyniku lintera to inna jakość niż agent sprawdzany raz w CI.

**② Duplikacja jest zagrożeniem numer jeden, nie złożoność.** Dane są
jednoznaczne: powielanie wzrosło o 81%, refaktoryzacja spadła pięciokrotnie.
Twoja obrona to `jscpd` w hooku przed commitem plus reguła 14 w `AGENTS.md`
plus metryka stosunku refaktoryzacji w raporcie tygodniowym.

**③ Przegląd wymaga listy kontrolnej, bo intuicja zawodzi.** Udokumentowano,
że recenzenci oceniają kod AI łagodniej mimo gorszej jakości projektowej.
Skoro jesteś jednocześnie autorem i recenzentem, ta skłonność będzie u ciebie
silniejsza, nie słabsza.

I jedno na koniec, wynikające z badań DORA: AI jest wzmacniaczem. Jeśli twoje
praktyki inżynierskie będą dobre, przyspieszy je. Jeśli będą słabe, przyspieszy
powstawanie bałaganu. Wszystko powyżej służy temu, żeby wzmacniać właściwą rzecz.
