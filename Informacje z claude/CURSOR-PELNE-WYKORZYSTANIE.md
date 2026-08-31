# Cursor — pełne wykorzystanie możliwości (stan: sierpień 2026)

Aktualizacja poprzednich rekomendacji. Część z nich zdezaktualizowała się
w ciągu ostatnich miesięcy.

---

# 1. ARCHITEKTURA SUBAGENTÓW — NAJWIĘKSZY ZYSK

## 1.1 Jak to działa

(cite index="55-1">Subagent otrzymuje prompt z całym potrzebnym kontekstem, pracuje autonomicznie i zwraca wiadomość końcową z wynikami. Subagenty startują z czystym kontekstem — agent nadrzędny musi zawrzeć w prompcie wszystkie istotne informacje, bo subagent nie ma dostępu do wcześniejszej historii rozmowy.</cite>

(cite index="55-1">Cursor zawiera trzy wbudowane subagenty: `explore` do przeszukiwania bazy kodu, `bash` do poleceń powłoki i `browser` do automatyzacji przeglądarki. Obsługują operacje kontekstochłonne automatycznie, nie wymagają konfiguracji. Zostały zaprojektowane na podstawie analizy rozmów, w których wyczerpywano okno kontekstu.</cite>

(cite index="55-1">Od wersji 2.5 subagenty mogą uruchamiać własne subagenty, tworząc drzewo skoordynowanej pracy — z ograniczeniem: subagent uruchomiony przez innego subagenta nie może uruchamiać kolejnych. Subagenty działające w tle zapisują wynik do `~/.cursor/subagents/`, skąd agent nadrzędny może sprawdzać postęp.</cite>

(cite index="56-1">Subagenty mogą teraz działać na własnych maszynach wirtualnych. Każdy dostaje odizolowaną kopię projektu z czystym kontekstem we własnym środowisku chmurowym. Pozwala to testować zmiany agenta nadrzędnego w świeżych środowiskach albo rozdzielić niezależne poprawki bez kolizji.</cite>

## 1.2 Sześć subagentów dla twojego projektu

Największa wartość leży w pierwszym — jest bezpośrednią odpowiedzią na dane
empiryczne z poprzedniej rewizji.

### `.cursor/subagents/lowca-duplikatow.md` ⚠ obowiązkowy przed implementacją

```markdown
---
name: lowca-duplikatow
description: Szuka istniejącej implementacji ZANIM powstanie nowa
tools: [explore, bash]
model: composer
---

Otrzymujesz opis funkcjonalności do zaimplementowania.

Twoje jedyne zadanie: ustalić, czy coś podobnego już istnieje w repozytorium.

1. Przeszukaj `backend/app/services/`, `repositories/`, `domain/`
   pod kątem podobnej logiki — semantycznie, nie tylko po nazwie.
2. Sprawdź `frontend/src/features/` i `components/`.
3. Sprawdź `docs/GLOSSARY.md` — czy pojęcie ma już nazwę i implementację.
4. Uruchom `jscpd --min-lines 5` na kandydatach.

Zwróć:
- ISTNIEJE: ścieżka, nazwa, czy da się rozszerzyć zamiast pisać nowe
- PODOBNE: co jest blisko i czy warto wyodrębnić wspólną część
- BRAK: potwierdzenie, że trzeba napisać od zera

Nie pisz kodu. Nie proponuj implementacji.
```

**Dlaczego to jest najważniejszy subagent w zestawie:** badania pokazują, że
agenty powielają kod, bo ich okno kontekstu nie pokazuje istniejącego helpera.
Subagent z czystym kontekstem i jednym zadaniem — przeszukać — rozwiązuje
dokładnie tę przyczynę. Duplikacja wzrosła o 81%; to jest mechanizm obrony
u źródła, nie po fakcie w CI.

### `.cursor/subagents/weryfikator.md`

Wzorzec sugerowany wprost przez dokumentację: (cite index="55-1">subagent weryfikujący ma walidować ukończoną pracę, sprawdzać funkcjonalność implementacji, uruchamiać testy i raportować, co przeszło, a co jest niekompletne.</cite>

```markdown
---
name: weryfikator
description: Sprawdza ukończony plaster wobec kryteriów akceptacji
tools: [bash]
model: composer
---

Otrzymujesz: ścieżkę do delta-spec i listę zmienionych plików.

1. `just check` → styl i typy
2. `just test` → testy, pokrycie
3. `just arch` → import-linter
4. `just perf` → budżety wydajności
5. `just migrate-down` → migracja w obie strony
6. Przeczytaj kryteria akceptacji z delta-spec i sprawdź każde osobno

Zwróć tabelę: kryterium → PRZESZŁO / NIE / NIE DA SIĘ SPRAWDZIĆ.
Przy NIE podaj dokładny komunikat błędu.
Nie naprawiaj. Tylko raportuj.
```

### `.cursor/subagents/audytor-wydajnosci.md`

```markdown
---
name: audytor-wydajnosci
tools: [bash]
---

Dla każdego nowego lub zmienionego zapytania do tabel > 10k wierszy:
1. EXPLAIN (ANALYZE, BUFFERS) na bazie deweloperskiej z 50k rate_line
2. Wykryj Seq Scan, Nested Loop na dużych zbiorach, sortowanie na dysku
3. py-spy record przy przekroczeniu budżetu

Zwróć: zapytanie → plan → werdykt → sugerowany indeks.
```

### `.cursor/subagents/kronikarz.md` (tło)

```markdown
---
name: kronikarz
description: Aktualizuje dokumentację po zakończeniu plastra
tools: [bash]
background: true
---

1. Scal delta-spec z docs/deltas/open/ do docs/spec/<moduł>.md
2. Przenieś deltę do docs/deltas/archived/
3. Dopisz linię do docs/state/PROGRESS.md
4. Jeśli decyzja architektoniczna — utwórz szkic ADR
5. `just api-types` jeśli zmieniło się API

Nie dotykaj kodu produkcyjnego.
```

Działa w tle, nie zajmuje kontekstu głównego agenta.

### `.cursor/subagents/testolog.md`

```markdown
---
name: testolog
description: Pisze testy z delta-spec, bez implementacji
tools: [explore]
---

Z kryteriów akceptacji w delta-spec napisz testy, które MUSZĄ FAILOWAĆ.
Reguły biznesowe: property-based przez hypothesis.
Nowa tabela: test izolacji tenantów.
Nazwa testu to zdanie opisujące regułę.
Nie pisz implementacji. Nie modyfikuj kodu produkcyjnego.
```

### `.cursor/subagents/migrator.md`

```markdown
---
name: migrator
description: Migracje bazy z dostępem do MCP Postgres
tools: [bash, mcp__postgres]
---

Zawsze najpierw sprawdź aktualny schemat przez MCP.
Każda tabela: organization_id, RLS, test izolacji.
Zmiany wstecznie zgodne: dodaj → przepnij → usuń, trzy migracje.
Indeksy CONCURRENTLY na tabelach z danymi.
Uzasadnienie indeksu w komentarzu migracji.
```

## 1.3 Rój na izolowanych maszynach

Przy plastrach niezależnych — na przykład ósma faza, gdzie moduły drogowy,
kolejowy i drobnicowy nie mają wspólnych plików — możesz uruchomić trzy
subagenty na osobnych maszynach wirtualnych z odizolowanymi kopiami projektu.
Każdy pracuje bez kolizji, wyniki scalasz osobno.

Sprawdzi się też do testowania: subagent na czystej maszynie weryfikuje zmiany
agenta głównego w świeżym środowisku, co wyłapuje zależności od lokalnego stanu.

---

# 2. CUSTOM MODES — SKILLS JAKO TRYB STAŁY

(cite index="56-1">Dowolnej umiejętności można użyć jako trybu własnego: umiejętność zostaje przypięta do czatu. Tryby własne utrzymują agenta skupionego na jednej umiejętności — to jak „zawsze włączone" skille. Z menu `/` wybierasz skill i wciskasz Opt+Enter, albo wybierasz „Use as Mode".</cite>

To zmienia sposób, w jaki wykorzystujesz Skills z poprzedniej rewizji.

**Zamiast** wywoływać `/nowy-modul` przy każdej wiadomości —
**przypinasz go jako tryb na całą sesję plastra.** Agent trzyma się procedury
bez przypominania, a ty nie tracisz tokenów na powtarzanie instrukcji.

| Tryb przypięty | Kiedy |
|---|---|
| `plaster` | cała sesja realizacji plastra |
| `migracja-rls` | sesja pracy nad schematem |
| `adapter-armatora` | dodawanie kanału do M-19 |
| `ekstraktor` | praca nad pipeline M-20 |
| `refaktor` | slot refaktoryzacyjny co cztery tygodnie |
| `debug-wydajnosci` | gdy budżet przekroczony |

---

# 3. `/goal` — CEL DŁUGOTERMINOWY

(cite index="57-1">Polecenie `/goal` nadaje agentowi długotrwały cel, do którego dąży aż do pełnego ukończenia. Można je łączyć z trybem własnym, żeby agent podążał za playbookiem, albo z `/loop`, żeby wracał do sprawy cyklicznie.</cite>

Zastosowanie u ciebie — cel to warunek ukończenia plastra:

```
/goal Plaster 2.4 (M-21, silnik wyceny) przechodzi `just gate`
      i spełnia wszystkie kryteria z docs/deltas/open/2.4.md.
      Budżet: p95 poniżej 300 ms na 50 tysiącach rate_line.
```

Z przypiętym trybem `plaster` agent zna procedurę, a `/goal` trzyma go przy
celu przez całą sesję. To zastępuje ręczne pilnowanie „czy już skończył".

---

# 4. AUTOMATIONS — AGENTY ZDARZENIOWE

(cite index="57-1">Agenty chmurowe subskrybują źródło zdarzeń i budzą się, gdy coś się dzieje. Automatycznie subskrybują pull requesty, które utworzyły, i doprowadzają je do końca, naprawiając CI i odpowiadając na komentarze botów.</cite>

## 4.1 Sześć automatyzacji dla twojego projektu

| Automatyzacja | Wyzwalacz | Co robi |
|---|---|---|
| **Strażnik bramki** | PR otwarty/zmieniony | Uruchamia `just gate`, komentuje wynik, naprawia trywialne błędy |
| **Recenzent z listą kontrolną** | PR otwarty | Przechodzi listę z rewizji badawczej: duplikacja, maskowanie błędów, dryf złożoności, czy testy sprawdzają regułę |
| **Raport jakości** | cron, piątek | Duplikacja, stosunek refaktoryzacji, trend złożoności, przeżywalność problemów → moduł M-71 |
| **Triage zależności** | PR od Renovate | Ocenia ryzyko aktualizacji, uruchamia testy, scala bezpieczne |
| **Strażnik budżetów** | cron, nocny | `just perf` na gałęzi głównej, alert przy regresji |
| **Kontrakty armatorów** | cron, tygodniowy | Testy kontraktowe API armatorów — wykrywa zmianę u nich zanim zepsuje produkcję |

Ostatnia jest specyficzna dla twojej domeny i szczególnie wartościowa: API
armatorów zmieniają się bez zapowiedzi, a wykrycie tego w poniedziałek rano
jest znacznie tańsze niż w środku wyceny dla klienta.

## 4.2 Computer use — dowód wizualny

(cite index="59-1">Computer use pozwala agentom chmurowym uruchomionym przez automatyzację korzystać z komputera tak jak programista: obsługiwać przeglądarkę, robić zrzuty ekranu lub nagrania, korzystać z usług wewnętrznych. Jest włączone domyślnie dla każdej automatyzacji. Można poprosić agenta o demonstrację — na przykład o krótkie nagranie ekranu po zmianie w przepływie widocznym dla użytkownika.</cite>

Zastosowanie: automatyzacja po każdej zmianie w `features/quotation/` nagrywa
przejście ścieżki zapytanie → wycena → wysyłka i dołącza do PR. Masz dowód
wizualny zamiast deklaracji, że działa — i regresję wizualną widzisz od razu.

---

# 5. MEMORIES — I OSTRZEŻENIE SPECYFICZNE DLA TWOJEGO PRODUKTU

(cite index="58-1">Pamięci pozwalają agentowi czytać i zapisywać trwałe notatki między uruchomieniami tej samej automatyzacji. Każda pamięć jest przechowywana jako nazwany wpis, domyślnie `MEMORIES.md`, istniejący poza systemem plików agenta.</cite>

**Ostrzeżenie z dokumentacji, które w twoim przypadku jest kluczowe:**

(cite index="58-1">Pamięci utrzymują się między uruchomieniami i należy ich używać ostrożnie, jeśli automatyzacja obsługuje niezaufane dane wejściowe. Dane wejściowe mogą prowadzić do mylących albo złośliwych pamięci, które nieumyślnie wpłyną na przyszłe uruchomienia automatyzacji.</cite>

Twój pipeline ekstrakcji przetwarza cenniki od nieznanych agentów — czyli
dokładnie niezaufane wejście, o którym mowa. Prompt injection w komórce Excela
mógłby trafić do trwałej pamięci automatyzacji i wpływać na kolejne uruchomienia.

**Reguła do wpisania w konfigurację:**

> Automatyzacje mające kontakt z danymi z pipeline'u ekstrakcji (M-20) mają
> pamięci **wyłączone**. Bez wyjątków. Pamięci włączone tylko w automatyzacjach
> operujących na własnym kodzie i metrykach.

To jest niuans, którego łatwo nie zauważyć, a konsekwencje byłyby trudne do
wykrycia.

---

# 6. AUTO-REVIEW I SANDBOX

(cite index="53-1">Auto-review to tryb pozwalający agentom pracować dłużej z mniejszą liczbą ręcznych zatwierdzeń. Wywołania z listy dozwolonych uruchamiają się natychmiast, wywołania nadające się do izolacji trafiają do piaskownicy, a wszystko pozostałe idzie do subagenta klasyfikującego, który decyduje o zezwoleniu, przekierowaniu lub prośbie o zatwierdzenie. Tryb dotyczy wywołań powłoki, MCP i pobierania.</cite>

(cite index="61-1">Cursor uruchamia polecenia powłoki w piaskownicy domyślnie na macOS. Polecenia w piaskownicy mają dostęp do odczytu i zapisu w przestrzeni roboczej, ale nie mają dostępu do internetu, chyba że zostanie dodany do listy dozwolonych.</cite>

**Twoja konfiguracja listy dozwolonych:**

```json
{
  "autoReview": {
    "allowlist": [
      "just check", "just test", "just arch", "just perf",
      "just migrate", "just migrate-down", "just api-types",
      "ruff *", "mypy *", "pytest *", "alembic *",
      "pnpm test", "pnpm tsc *", "jscpd *"
    ],
    "sandbox": ["python *", "node *", "psql *"],
    "requireApproval": [
      "git push *", "docker *", "curl *", "rm *",
      "alembic downgrade *"
    ]
  }
}
```

Efekt: agent przechodzi całą pętlę weryfikacji bez pytania cię o zgodę przy
każdym `pytest`, ale nie wypchnie niczego do zdalnego repozytorium bez ciebie.

---

# 7. WYBÓR MODELU

(cite index="61-1">Do złożonych zadań wielopikowych najmocniejsze rozumowanie dają modele czołowe. Dla szybkości i efektywności kosztowej warto używać trybu Auto — Cursor sam dobiera model do każdego podzadania, a tryb Auto nie zużywa puli kredytów. Do dużych zadań warto przełączyć się na tryb planowania przed wykonaniem; można nawet planować agentami równoległymi, generując kilka planów do porównania przed wyborem jednego.</cite>

**Twoja strategia:**

| Zadanie | Model |
|---|---|
| Domyślnie | Auto — nie zużywa puli |
| Plaster rutynowy | Composer — szybki, wystarczający |
| Architektura, decyzja z ADR | model czołowy w trybie planowania |
| Refaktoryzacja wielu plików | model czołowy |
| Subagenty pomocnicze | Composer |

**Plany równoległe** wykorzystaj przy decyzjach z rejestru, gdzie było kilka
opcji — na przykład modelowanie `port_charge_rule` z jedenastoma wymiarami
warunkowymi. Wygeneruj trzy plany, porównaj, wybór udokumentuj jako ADR.

---

# 8. ZAKTUALIZOWANA PĘTLA PLASTRA

Wersja wykorzystująca wszystko powyżej:

```
① DELTA-SPEC        piszesz sam, 15 minut
                    docs/deltas/open/<id>.md

② TRYB + CEL        przypnij tryb `plaster` (Opt+Enter z /)
                    /goal <warunek ukończenia z delta-spec>

③ ŁOWCA DUPLIKATÓW  subagent, obowiązkowo przed kodem
                    → ISTNIEJE / PODOBNE / BRAK

④ PLAN              tryb planowania; przy decyzji architektonicznej
                    plany równoległe do porównania

⑤ TESTOLOG          subagent pisze testy z kryteriów akceptacji
                    → muszą failować

⑥ IMPLEMENTACJA     agent główny; hooki po każdej edycji zwracają
                    błędy lintera natychmiast

⑦ WERYFIKATOR       subagent uruchamia bramkę i sprawdza kryteria
                    → tabela: kryterium → werdykt

⑧ AUDYTOR WYDAJNOŚCI subagent: EXPLAIN na nowych zapytaniach

⑨ KRONIKARZ         subagent w tle: scala deltę do spec, PROGRESS.md,
                    api-types, szkic ADR

⑩ PR                automatyzacja: strażnik bramki + recenzent
                    + nagranie z computer use przy zmianie w UI
                    → nowa rozmowa
```

Twoja rola w tej pętli: kroki ① i ⑤ (weryfikacja, czy testy opisują właściwe
reguły) plus decyzja w ④. Reszta to nadzór.

---

# 9. CO DOPISAĆ DO KITU

```
.cursor/
├── subagents/
│   ├── lowca-duplikatow.md      ← obowiązkowy przed implementacją
│   ├── weryfikator.md
│   ├── testolog.md
│   ├── audytor-wydajnosci.md
│   ├── kronikarz.md             ← tło
│   └── migrator.md
├── skills/                       ← używane też jako Custom Modes
├── hooks/
├── plans/
├── mcp.json
└── settings.json                 ← auto-review allowlist
```

Plus w `AGENTS.md`, w sekcji „Jak pracujesz":

> Przed napisaniem nowej funkcji uruchom subagenta `lowca-duplikatow`.
> Po zakończeniu implementacji uruchom `weryfikator`.
> Nie raportuj ukończenia bez tabeli od weryfikatora.

---

# 10. TRZY RZECZY, KTÓRE ZMIENIAJĄ NAJWIĘCEJ

**① Łowca duplikatów jako krok obowiązkowy.** Badania wskazują duplikację jako
zagrożenie numer jeden, a przyczyną jest ograniczone okno kontekstu agenta.
Subagent z czystym kontekstem i jednym zadaniem usuwa przyczynę, a nie skutek.

**② Custom Mode plus `/goal` zamiast pilnowania.** Tryb trzyma procedurę, cel
trzyma kierunek. Przestajesz powtarzać instrukcje w każdym prompcie — to jest
zarazem oszczędność tokenów i mniejsza szansa na dryf.

**③ Pamięci wyłączone w automatyzacjach dotykających ekstrakcji.** Jedyne
ostrzeżenie bezpieczeństwa z tej listy, ale poważne: przetwarzasz niezaufane
pliki, a zatruta pamięć trwała jest trudna do wykrycia i wpływa na przyszłe
uruchomienia.
