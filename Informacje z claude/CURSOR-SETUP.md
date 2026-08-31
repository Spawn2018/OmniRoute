# Konfiguracja Cursora i środowiska

---

# 1. NAJPIERW: SKOMPILUJ DOKUMENTACJĘ

Szesnaście aneksów w obecnej formie to około 300 tysięcy znaków. Wrzucone do
kontekstu zjedzą budżet, zanim agent napisze linijkę. Trzeba je przełożyć na
strukturę, z której pobiera się fragmenty na żądanie.

```
docs/
├── ARCHITECTURE.md          ← mapa repo, granice modułów, gdzie co leży   (~150 linii)
├── GLOSSARY.md              ← słownik domenowy PL/EN                       (~100 linii)
├── DECISIONS.md             ← rejestr rozstrzygnięć, jedna linia każde
├── spec/
│   ├── tenancy.md           ← wielodostępność, RLS, uprawnienia
│   ├── parties.md           ← kontrahenci, kontakty, rejestry PL
│   ├── charges.md           ← słownik opłat, kaskada narzutów
│   ├── rates-sheets.md      ← stawki z cenników, ekstrakcja
│   ├── rates-live.md        ← API armatorów, agregatorzy, kanały
│   ├── port-charges.md      ← opłaty portowe warunkowe
│   ├── quotation.md         ← silnik wyceny, waluty, luki
│   ├── rfq.md               ← zapytania klientów i do agentów
│   ├── shipment.md          ← zlecenia, statusy, dokumenty
│   ├── tracking.md          ← DCSA, wyjątki
│   ├── finance.md           ← koszt pieniądza, FX, rozliczenia
│   ├── road.md              ← moduł drogowy, alokacja, doładunki
│   ├── rail.md              ← kolej dowozowa i chińska
│   ├── lcl.md               ← drobnica morska
│   ├── compliance.md        ← sankcje, ADR, RODO
│   └── market.md            ← dane rynkowe, prognozy
├── adr/
│   └── NNNN-tytul.md        ← decyzje architektoniczne
└── state/
    ├── PROGRESS.md          ← log ukończonych plastrów, po jednej linii
    └── CURRENT.md           ← bieżące zadanie, kontekst, ustalenia
```

**Zasada rozmiaru: żaden plik w `spec/` nie przekracza 400 linii.** Jeśli przekracza,
dzielisz. Agent ma czytać jeden plik, nie pół książki.

**Jak skompilować:** to jest pierwsze zadanie dla Cursora. Wrzuć aneksy do
`docs/_source/`, i poproś o rozbicie na powyższą strukturę, moduł po module.
Potem `docs/_source/` przenieś poza repozytorium — służy tobie, nie agentowi.

---

# 2. PLIKI REGUŁ

## 2.1 `AGENTS.md` w katalogu głównym

Osobny plik, gotowy do skopiowania. To jest jedyna rzecz zawsze w kontekście.

## 2.2 `.cursor/rules/` — reguły z zakresem

Kluczowe dla oszczędności tokenów: reguła z `globs` wchodzi do kontekstu **tylko
wtedy**, gdy agent dotyka pasujących plików.

### `.cursor/rules/backend.mdc`

```markdown
---
description: Konwencje backendu Python
globs: ["backend/**/*.py"]
alwaysApply: false
---

## Warstwy — kierunek zależności tylko w dół

api → services → repositories → models
Warstwa nie importuje z warstwy wyżej. Egzekwowane przez import-linter.

## Reguły

- Endpointy nie zawierają logiki biznesowej. Wołają serwis i zwracają DTO.
- Serwis nie zna FastAPI. Bez `Request`, `Depends`, `HTTPException` w serwisach.
- Repozytorium nie zna reguł biznesowych. Tylko dostęp do danych.
- Każde zapytanie do bazy przechodzi przez repozytorium.
- Kwoty: `Decimal`, nigdy `float`. Typ `Money(amount, currency)` z py-moneyed.
- Daty: `pendulum`, świadome strefy czasowej. Bez naiwnych `datetime`.
- Async wszędzie, gdzie jest I/O. Bez blokujących wywołań w ścieżce żądania.
- Wyjątki domenowe w `domain/errors.py`, mapowane na HTTP w jednym miejscu.

## Zapytania

- Bez N+1. Relacje przez `selectinload`/`joinedload`, świadomie.
- Każda nowa migracja: przemyśl indeksy i zapisz uzasadnienie w komentarzu.
- Zapytania analityczne nie idą przez ORM. Surowy SQL w `repositories/analytics/`.
```

### `.cursor/rules/frontend.mdc`

```markdown
---
description: Konwencje frontendu
globs: ["frontend/**/*.{ts,tsx}"]
alwaysApply: false
---

- Komponent to jeden plik, jedna odpowiedzialność, poniżej 200 linii.
- Stan serwera wyłącznie przez TanStack Query. Bez `useEffect` do pobierania danych.
- Formularze: react-hook-form + zod. Schemat zod współdzielony z typami z OpenAPI.
- Typy API generowane z OpenAPI przez `hey-api/openapi-ts`. Nigdy ręcznie.
- Tabele: TanStack Table. Powyżej 1000 wierszy — wirtualizacja obowiązkowa.
- Komponenty z shadcn/ui kopiowane do `components/ui/`, modyfikowane u siebie.
- Bez `any`. Bez `as` poza parsowaniem odpowiedzi zewnętrznych.
- Dostępność: każdy interaktywny element osiągalny klawiaturą, focus widoczny.
- Skróty klawiszowe dla ścieżki zapytanie → wycena → wysyłka. To wymóg produktowy.
```

### `.cursor/rules/database.mdc`

```markdown
---
description: Baza danych i migracje
globs: ["backend/alembic/**", "backend/**/models/**"]
alwaysApply: false
---

- Każda tabela: `organization_id`, `created_at`, `updated_at`, `created_by`.
- Każda tabela: polityka RLS + test dowodzący izolacji tenantów.
- Kwoty: `Numeric(14, 4)`. Waluta: `CHAR(3)` obok, zawsze parami.
- Klucze obce z jawnym `ondelete`. Bez kaskad na danych finansowych.
- Migracja ma działać w górę i w dół. Test obu kierunków w CI.
- Zmiany wstecznie zgodne: najpierw dodaj kolumnę, potem przepnij kod,
  potem usuń starą. Nigdy w jednej migracji.
- Indeksy tworzone `CONCURRENTLY` na tabelach z danymi.
```

### `.cursor/rules/testing.mdc`

```markdown
---
description: Testy
globs: ["**/tests/**", "**/*.test.ts", "**/*_test.py"]
alwaysApply: false
---

- Testy reguł biznesowych pisane z wiedzy domenowej, nie generowane z implementacji.
- Postgres w testach przez testcontainers. Bez SQLite udającego Postgresa.
- Property-based (hypothesis) dla: przeliczeń walutowych, wagi obliczeniowej,
  kaskady narzutów, kosztu finansowania.
- Każda nowa tabela: test izolacji tenantów.
- Test nazywa się zdaniem opisującym regułę, nie funkcję.
  `test_chargeable_weight_uses_higher_of_tonnes_or_cbm`, nie `test_calc_1`.
- Bez mockowania własnego kodu. Mockuj wyłącznie granice zewnętrzne.
```

### `.cursor/rules/no-slop.mdc`

```markdown
---
description: Zakazy stylistyczne
alwaysApply: true
---

Kod ma wyglądać, jakby napisał go doświadczony programista, nie generator.

ZAKAZANE:
- Komentarze powtarzające kod: `# pobierz użytkownika` nad `get_user()`
- Docstringi opisujące oczywiste parametry bez wnoszenia informacji
- `try/except Exception` bez konkretnej obsługi
- Nadmiarowe warstwy abstrakcji: fabryki, interfejsy z jedną implementacją
- Nazwy typu `data`, `result`, `temp`, `handler`, `manager`, `helper`
- Emoji, ozdobniki ASCII, banery komentarzowe
- Kod zakomentowany „na wszelki wypadek"
- Defensywne sprawdzanie `if x is not None` tam, gdzie typ tego nie dopuszcza

WYMAGANE:
- Komentarz wyjaśnia decyzję: `# NBP tabela A z D-1, wymóg ustawy o VAT`
- Nazwy z domeny: `chargeable_weight`, nie `calc_weight`
- Wczesne wyjścia zamiast zagnieżdżonych warunków
```

## 2.3 Reguła kontekstu — najważniejsza dla kosztu

### `.cursor/rules/context.mdc`

```markdown
---
description: Zarządzanie kontekstem
alwaysApply: true
---

Zanim zaczniesz zadanie:

1. Przeczytaj `docs/state/CURRENT.md` — tam jest zakres i ustalenia.
2. Przeczytaj TYLKO ten plik ze `spec/`, który dotyczy zadania.
3. Strukturę bazy sprawdź przez MCP Postgres, nie czytając wszystkich modeli.
4. Nie przeszukuj repozytorium „na wszelki wypadek". Mapa jest w ARCHITECTURE.md.

Jeśli brakuje ci informacji — zapytaj. Nie zgaduj i nie czytaj kolejnych plików
w nadziei, że znajdziesz.

Po zakończeniu: jedna linia w `docs/state/PROGRESS.md`, aktualizacja `CURRENT.md`.
```

---

# 3. SERWERY MCP

Podłącz w `.cursor/mcp.json`. Każdy zmniejsza liczbę błędów i zużycie tokenów.

| Serwer | Co daje | Dlaczego istotny |
|---|---|---|
| **Postgres MCP** | Odczyt schematu i zapytania na bazie deweloperskiej | Agent przestaje zgadywać nazwy kolumn. Największa pojedyncza poprawa trafności |
| **Context7** | Aktualna dokumentacja bibliotek wstrzykiwana do kontekstu | Wiedza modelu o bibliotekach się starzeje. To eliminuje wymyślone API |
| **GitHub MCP** | Issues, PR, historia | Praca na zadaniach bez przeklejania |
| **Playwright MCP** | Sterowanie przeglądarką | Agent sam sprawdza, czy interfejs działa |
| **Sentry MCP** | Błędy produkcyjne | Naprawa od zgłoszenia, nie od opisu |

**Context7 zasługuje na wyróżnienie.** Twój stos to biblioteki, które zmieniają API
między wersjami. Bez aktualnej dokumentacji agent napisze kod pod wersję sprzed
dwóch lat — i będzie działał, tylko gorzej i niezgodnie z obecnymi praktykami.

---

# 4. TRYB PRACY: PROMPT CZY AGENT

Odpowiedź: **oba, ale do różnych rzeczy.**

| Sytuacja | Tryb | Uzasadnienie |
|---|---|---|
| Nowy plaster funkcjonalny | **Plan → Agent** | Najpierw plan w trybie planowania, akceptujesz, potem wykonanie |
| Refaktoryzacja wielu plików | **Agent** | Potrzebuje kontekstu całego zakresu |
| Poprawka w jednym pliku | **Inline (Cmd+K)** | Najtańsze, bez ładowania kontekstu |
| Pytanie o kod | **Chat, tryb Ask** | Bez uprawnień do zapisu |
| Migracja bazy | **Agent + Postgres MCP** | Musi zobaczyć aktualny schemat |
| Trudny błąd | **Chat z hipotezami**, potem inline | Agent lubi „naprawić" przyczynę objawu |

## Pętla robocza jednego plastra

```
1. PLAN       Tryb planowania. „Przeczytaj docs/spec/quotation.md sekcja 4.
              Zaplanuj plaster: silnik doboru stawek. Nie pisz kodu."
              → czytasz plan, poprawiasz, akceptujesz

2. TEST       „Napisz testy do planu. Bez implementacji."
              → weryfikujesz, czy testy opisują właściwe reguły

3. IMPL       „Zaimplementuj tak, żeby testy przeszły."

4. WERYFIKACJA  just check && just test && just arch

5. PRZEGLĄD   PR → automatyczny recenzent → poprawki

6. ZAPIS      Jedna linia w PROGRESS.md, wyczyszczenie kontekstu
```

**Punkt szósty jest krytyczny dla kosztu.** Nowy plaster to nowa rozmowa.
Ciągnięcie jednego wątku przez tydzień oznacza, że każdy prompt niesie
historię, której agent nie potrzebuje.

---

# 5. BRAMKI JAKOŚCI — DŁUG TECHNICZNY BLOKOWANY MASZYNOWO

Dyscyplina nie działa. Działa CI, który nie przepuszcza.

## 5.1 Granice modułów — `import-linter`

Najważniejsze narzędzie w tej sekcji i najrzadziej używane.

`.importlinter`:
```ini
[importlinter]
root_package = app

[importlinter:contract:layers]
name = Warstwy
type = layers
layers =
    app.api
    app.services
    app.repositories
    app.models

[importlinter:contract:modules]
name = Moduły niezależne
type = independence
modules =
    app.modules.rates
    app.modules.quotation
    app.modules.shipment
    app.modules.finance
```

Próba zaimportowania serwisu wyceny w repozytorium stawek wywala CI. To jest
mechanizm, który utrzyma modułowość, gdy zabraknie czasu i uwagi.

## 5.2 Pozostałe bramki

| Narzędzie | Blokuje |
|---|---|
| `ruff` + `mypy --strict` | styl, typy |
| `pytest --cov --cov-fail-under=80` | brak testów |
| `import-linter` | naruszenie architektury |
| `schemathesis` | niezgodność API z OpenAPI |
| `testcontainers` | testy na nieprawdziwej bazie |
| `k6` z progami | regresja wydajności |
| Lighthouse CI | regresja frontendu |
| `trufflehog` | sekrety w kodzie |
| `renovate` | zaległości w zależnościach |
| `pr-agent` | brak przeglądu |
| `commitlint` | bałagan w historii |

## 5.3 Test izolacji tenantów — obowiązkowy wzorzec

```python
async def test_rate_lines_isolated_between_tenants(db, org_a, org_b):
    await create_rate_line(db, org_a, pol="PLGDY", pod="CNSHA")

    async with tenant_context(db, org_b):
        result = await RateLineRepository(db).find(pol="PLGDY")

    assert result == []
```

Ten test powtarzasz dla każdej nowej tabeli. Bez niego nie masz produktu
wielodostępnego, tylko nadzieję.

---

# 6. DOKUMENTACJA TWORZĄCA SIĘ SAMA

| Warstwa | Narzędzie | Wyzwalacz |
|---|---|---|
| API | FastAPI → OpenAPI → `scalar` | automatycznie z kodu |
| Klient TS | `hey-api/openapi-ts` | przy każdej zmianie API |
| Baza | `azimutt` / `dbml` | z migracji |
| Kod | `mkdocs-material` + `mkdocstrings` | z docstringów |
| Decyzje | ADR w `docs/adr/` | reguła: każda decyzja architektoniczna = ADR |
| Zmiany | `release-please` | z commitów |

**Reguła w CI:** zmiana w `backend/app/services/**` bez zmiany w `docs/spec/**`
generuje ostrzeżenie w PR. Nie blokuje, ale widać.

---

# 7. WYDAJNOŚĆ OD PIERWSZEGO DNIA

Refaktoryzacja pod wydajność po fakcie jest droga. Budżety wpisane w CI są tanie.

```python
# tests/perf/test_quote_engine.py
@pytest.mark.perf
async def test_quote_from_stored_rates_under_300ms(bench, seeded_rates_50k):
    result = await bench(quote_engine.run, sample_request)
    assert result.p95_ms < 300
```

Do tego:
- `pg_stat_statements` włączone od początku, przegląd najwolniejszych zapytań co tydzień
- `py-spy` przy każdym przekroczeniu budżetu — profil zamiast zgadywania
- budżet rozmiaru paczki frontendu w CI
- `k6` na kluczowych endpointach, progi jako testy

**Reguła:** przekroczenie budżetu to błąd blokujący, nie zadanie na później.
Tak nie powstaje dług.

---

# 8. NARZĘDZIA PONAD CURSOREM

| Narzędzie | Do czego |
|---|---|
| **Claude Code** | Zadania wielopikowe, migracje przez całe repo, refaktoryzacje, których Cursor nie unosi |
| **`github/spec-kit`** | Development sterowany specyfikacją — twoje `docs/spec/` jako źródło prawdy |
| **`qodo-ai/pr-agent`** | Automatyczny przegląd PR. Piszesz sam, nie masz kto cię sprawdzić |
| **`PatrickJS/awesome-cursorrules`** | Gotowe reguły do adaptacji |
| **Neon** | Gałąź bazy per PR — testujesz migrację na realnych danych |
| **`azimuttapp/azimutt`** | Wizualizacja schematu przy 40 tabelach |
| **Storybook** | Komponenty w izolacji, katalog interfejsu |
| **`renovatebot/renovate`** | Aktualizacje zależności |

---

# 9. PIERWSZE TRZY DNI

**Dzień 1 — szkielet**
1. `fastapi/full-stack-fastapi-template` jako punkt startowy
2. `AGENTS.md`, `.cursor/rules/`, `.importlinter`, `justfile`
3. Docker Compose: Postgres, Redis, MinIO, Mailpit
4. CI: ruff, mypy, pytest, import-linter — puste, ale przechodzące

**Dzień 2 — kompilacja dokumentacji**
5. Aneksy do `docs/_source/`, zadanie dla Cursora: rozbicie na `docs/spec/`
6. `ARCHITECTURE.md`, `GLOSSARY.md` — ręcznie, to jest twoja wiedza
7. MCP: Postgres, Context7, GitHub

**Dzień 3 — pierwszy plaster**
8. Migracja: `organization`, `app_user`, RLS
9. Test izolacji tenantów — pierwszy i wzorcowy
10. Jeden endpoint od końca do końca, z testem i typem na froncie

Po trzecim dniu masz pętlę, która się powtarza dla każdego kolejnego plastra.
Reszta to sto powtórzeń tego samego cyklu.
