# Zestaw konfiguracyjny — pliki do wrzucenia do repozytorium

Wszystko poniżej to gotowa treść. Kopiujesz pod wskazane ścieżki.

---

# 1. STRUKTURA REPOZYTORIUM

```
.
├── AGENTS.md                    ← konstytucja, zawsze w kontekście
├── justfile                     ← wszystkie komendy
├── .importlinter                ← kontrakty architektoniczne
├── .cursor/
│   ├── mcp.json
│   └── rules/
│       ├── context.mdc          alwaysApply
│       ├── no-slop.mdc          alwaysApply
│       ├── backend.mdc          globs: backend/**/*.py
│       ├── database.mdc         globs: backend/alembic/**, **/models/**
│       ├── frontend.mdc         globs: frontend/**/*.{ts,tsx}
│       ├── testing.mdc          globs: **/tests/**
│       ├── performance.mdc      globs: **/services/**, **/repositories/**
│       └── workflows.mdc        globs: backend/**/workflows/**
├── docs/
│   ├── ARCHITECTURE.md
│   ├── MODULES.md               ← rejestr M-01…M-70
│   ├── GLOSSARY.md
│   ├── spec/                    ← 70 plików, każdy < 400 linii
│   ├── adr/
│   └── state/
│       ├── CURRENT.md
│       └── PROGRESS.md
├── backend/
│   └── app/
│       ├── api/                 ← routery, DTO, bez logiki
│       ├── services/            ← logika domenowa, nie zna FastAPI
│       ├── repositories/        ← dostęp do danych, nie zna reguł
│       ├── models/              ← SQLAlchemy
│       ├── domain/              ← typy, wyjątki, wartości
│       ├── workflows/           ← Temporal
│       └── integrations/        ← adaptery zewnętrzne
└── frontend/
    └── src/
        ├── features/<moduł>/    ← pion per moduł, nie per typ pliku
        ├── components/ui/       ← shadcn, skopiowane
        ├── lib/
        └── api/                 ← generowane z OpenAPI, nie edytuj
```

**Frontend organizowany pionowo per moduł, nie poziomo per typ.**
`features/quotation/` zawiera komponenty, hooki, typy i testy wyceny.
To znacząco zmniejsza kontekst potrzebny agentowi przy zadaniu.

---

# 2. REGUŁY CURSORA

## `.cursor/rules/context.mdc`

```markdown
---
description: Zarządzanie kontekstem i tokenami
alwaysApply: true
---

Przed zadaniem:
1. Przeczytaj `docs/state/CURRENT.md` — zakres, moduł, ustalenia.
2. Przeczytaj TYLKO ten plik ze `spec/`, który wskazuje CURRENT.md.
3. Schemat bazy — przez MCP Postgres, nie przez czytanie modeli.
4. Struktura repo — `docs/ARCHITECTURE.md`, nie przeszukiwanie.

NIE RÓB:
- Nie czytaj plików „żeby zrozumieć kontekst". Kontekst jest w CURRENT.md.
- Nie przeszukuj repozytorium rekurencyjnie.
- Nie otwieraj więcej niż jednego pliku spec.
- Nie zgaduj nazw kolumn ani endpointów.

Brakuje informacji → zapytaj jednym pytaniem. Nie eksploruj.

Po zadaniu: linia w PROGRESS.md, aktualizacja CURRENT.md, koniec.
```

## `.cursor/rules/no-slop.mdc`

```markdown
---
description: Kod ma wyglądać na napisany przez człowieka
alwaysApply: true
---

ZAKAZANE BEZWZGLĘDNIE:
- Komentarz powtarzający kod: `# pobierz użytkownika` nad `get_user()`
- Docstring wypisujący parametry bez wnoszenia informacji
- `try/except Exception` bez konkretnej obsługi
- Nazwy: data, result, temp, item, obj, handler, manager, helper, utils
- Fabryki, interfejsy i warstwy z jedną implementacją
- Emoji, banery ASCII, ozdobne separatory komentarzowe
- Kod zakomentowany „na wszelki wypadek"
- `if x is not None` tam, gdzie typ tego nie dopuszcza
- Powtarzanie tej samej walidacji w trzech warstwach

WYMAGANE:
- Komentarz uzasadnia decyzję: `# NBP D-1 roboczy — wymóg ustawy o VAT art. 31a`
- Nazwy z GLOSSARY.md: chargeable_weight, nie calc_weight
- Wczesne wyjścia zamiast zagnieżdżeń
- Jedna funkcja = jedna odpowiedzialność
- Wyjątki domenowe z domain/errors.py, mapowane na HTTP w jednym miejscu
```

## `.cursor/rules/backend.mdc`

```markdown
---
description: Backend
globs: ["backend/**/*.py"]
---

WARSTWY — zależności tylko w dół, egzekwowane przez import-linter:
api → services → repositories → models
workflows → services (nigdy odwrotnie)
integrations → domain (nigdy do services)

- Endpoint: walidacja, wywołanie serwisu, mapowanie DTO. Zero logiki.
- Serwis nie zna FastAPI. Bez Request, Depends, HTTPException.
- Repozytorium nie zna reguł biznesowych.
- Każde zapytanie do bazy przez repozytorium.
- Kwoty: Money(Decimal, Currency). Bez gołych liczb w domenie.
- Daty: pendulum ze strefą. Bez naiwnych datetime.
- Async przy I/O. Bez blokujących wywołań w ścieżce żądania.
- Wywołania zewnętrzne: idempotencja + retry z backoffem + timeout.
- Zdarzenia dla innych modułów: przez outbox, nie bezpośrednie wywołanie.

ZAPYTANIA (zasada 11):
- Filtrowanie i agregacja w SQL, nie w Pythonie.
- Ścieżki gorące (silnik wyceny): asyncpg + surowy SQL, nie ORM.
- Relacje: selectinload/joinedload świadomie. N+1 to błąd blokujący.
- Nowa migracja: przemyśl indeks, zapisz uzasadnienie w komentarzu migracji.
```

## `.cursor/rules/database.mdc`

```markdown
---
description: Baza i migracje
globs: ["backend/alembic/**", "backend/app/models/**"]
---

- Każda tabela: organization_id, created_at, updated_at, created_by.
- Każda tabela: polityka RLS + test izolacji. Bez wyjątków.
- Kwoty: Numeric(14,4) + CHAR(3) waluta obok. Zawsze parami.
- Klucze obce z jawnym ondelete. Bez kaskad na danych finansowych.
- Migracja działa w górę i w dół. Oba kierunki testowane.
- Zmiany wstecznie zgodne: dodaj kolumnę → przepnij kod → usuń starą.
  Trzy migracje, nigdy jedna.
- Indeksy CONCURRENTLY na tabelach z danymi.
- Tabele dystrybuowane (Citus) kluczem organization_id — projektuj tak,
  żeby żadne złączenie nie przekraczało granicy tenanta.
- Widoki materializowane na ścieżkach gorących, odświeżane zdarzeniem.
```

## `.cursor/rules/frontend.mdc`

```markdown
---
description: Frontend
globs: ["frontend/**/*.{ts,tsx}"]
---

STRUKTURA: features/<moduł>/ zawiera komponenty, hooki, typy, testy modułu.
Współdzielone tylko w components/ui/ i lib/.

- Stan serwera wyłącznie TanStack Query. Bez useEffect do pobierania.
- Typy API generowane przez openapi-ts. Katalog api/ jest tylko do odczytu.
- Formularze: react-hook-form + zod. Schemat zod z typów OpenAPI.
- Tabele: TanStack Table. Powyżej 500 wierszy wirtualizacja obowiązkowa.
- Kwoty: komponent <Money/>. Nigdy surowy number w JSX.
  Tabular numerals, wyrównanie do prawej, separator tysięcy per locale.
- Bez any. as tylko przy parsowaniu odpowiedzi zewnętrznych.
- Każdy interaktywny element osiągalny klawiaturą, focus widoczny.
- Skróty klawiszowe rejestrowane centralnie w lib/shortcuts.
- Stany: loading, empty, error i partial to komponenty pierwszej klasy,
  nie warunki inline.
- Import z barrel files zabroniony — psuje tree shaking.
```

## `.cursor/rules/performance.mdc`

```markdown
---
description: Wydajność
globs: ["backend/app/services/**", "backend/app/repositories/**"]
---

- Przed napisaniem zapytania: ile wierszy zwróci przy 50k rate_line?
- Zapytanie zwracające ponad 1000 wierszy do Pythona wymaga uzasadnienia.
- Agregacja, sortowanie i filtrowanie zawsze w SQL.
- Wywołania zewnętrzne równolegle (asyncio.gather) z timeoutem.
- Cache: Redis z kluczem zawierającym organization_id i wersję danych.
- Każdy nowy endpoint w ścieżce krytycznej: test wydajnościowy z progiem.
- EXPLAIN ANALYZE na nowym zapytaniu do rate_line — dołącz do PR.
```

## `.cursor/rules/testing.mdc`

```markdown
---
description: Testy
globs: ["**/tests/**", "**/*.test.ts", "**/*_test.py"]
---

- Reguły biznesowe: testy pisane z wiedzy domenowej, nie z implementacji.
- Postgres przez testcontainers. Nigdy SQLite.
- Property-based (hypothesis): przeliczenia walutowe, waga obliczeniowa,
  kaskada narzutów, koszt finansowania, alokacja kosztu przejazdu.
- Każda nowa tabela: test izolacji tenantów.
- Integracje zewnętrzne: pact (kontrakt) + wiremock (zachowanie).
- Nazwa testu to zdanie opisujące regułę:
  test_chargeable_weight_uses_higher_of_tonnes_or_cbm
- Bez mockowania własnego kodu. Mockuj wyłącznie granice.
- Test wydajnościowy dla każdej ścieżki z budżetem w AGENTS.md.
```

## `.cursor/rules/workflows.mdc`

```markdown
---
description: Workflow Temporal
globs: ["backend/app/workflows/**"]
---

- Workflow jest deterministyczny. Bez random, datetime.now, I/O.
  Czas przez workflow.now(), losowość przez workflow.random().
- I/O wyłącznie w activities. Activity idempotentna.
- Timery przez workflow.sleep i wait_condition, nigdy asyncio.sleep.
- Sygnały do przyjmowania zdarzeń zewnętrznych (odpowiedź agenta).
- Kompensacja jawna dla operacji z efektem zewnętrznym (booking).
- Wersjonowanie workflow przy zmianie logiki — patch, nie nadpisanie.
```

---

# 3. `.importlinter`

```ini
[importlinter]
root_package = app
include_external_packages = True

[importlinter:contract:warstwy]
name = Warstwy
type = layers
layers =
    app.api
    app.workflows
    app.services
    app.repositories
    app.models

[importlinter:contract:moduly]
name = Niezależność modułów domenowych
type = independence
modules =
    app.services.rates
    app.services.quotation
    app.services.shipment
    app.services.finance
    app.services.compliance
    app.services.extraction

[importlinter:contract:integracje]
name = Integracje nie znają serwisów
type = forbidden
source_modules = app.integrations
forbidden_modules = app.services

[importlinter:contract:domena]
name = Domena bez zależności zewnętrznych
type = forbidden
source_modules = app.domain
forbidden_modules = fastapi, sqlalchemy, httpx
```

---

# 4. `justfile`

```make
default: check test

# --- codzienne ---
dev:            docker compose up -d && granian --interface asgi app.main:app --reload
check:          ruff check . && ruff format --check . && mypy app && cd frontend && pnpm lint && pnpm tsc --noEmit
fix:            ruff check --fix . && ruff format . && cd frontend && pnpm lint --fix
test:           pytest -x --cov=app --cov-fail-under=80 && cd frontend && pnpm test
arch:           lint-imports
perf:           pytest -m perf && k6 run tests/perf/quote.js
audit:          pip-audit && pnpm audit && trufflehog filesystem . && trivy fs .

# --- baza ---
migrate:        alembic upgrade head
migrate-down:   alembic downgrade -1 && alembic upgrade head
migration name: alembic revision --autogenerate -m "{{name}}"
schema:         atlas schema inspect --url $DATABASE_URL --format '{{ sql . }}'
seed:           python -m app.cli seed

# --- generowanie ---
api-types:      python -m app.cli openapi > openapi.json && cd frontend && pnpm openapi-ts
docs:           mkdocs build && just api-types
erd:            azimutt export --url $DATABASE_URL

# --- jakość ---
complexity:     ruff check --select C901 .
dead:           vulture app && cd frontend && knip
dup:            jscpd backend/app frontend/src
profile file:   py-spy record -o profile.svg -- python {{file}}

# --- pełna bramka, to samo co CI ---
gate:           just check && just test && just arch && just perf && just migrate-down && just docs
```

---

# 5. CI — `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test }
        options: >-
          --health-cmd pg_isready --health-interval 5s
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --all-extras

      - name: Styl i typy
        run: just check

      - name: Architektura
        run: just arch

      - name: Migracje w obie strony
        run: just migrate-down

      - name: Testy
        run: just test

      - name: Izolacja tenantów
        run: pytest -m tenant_isolation --strict-markers

      - name: Wydajność
        run: just perf

      - name: Bezpieczeństwo
        run: just audit

      - name: Rozmiar paczki
        run: cd frontend && pnpm build && npx size-limit

      - name: Dostępność
        run: cd frontend && pnpm test:a11y

      - name: Spec zaktualizowana
        run: python scripts/check_spec_sync.py
```

`check_spec_sync.py` sprawdza, czy zmiana w `services/<moduł>/` ma
odpowiadającą zmianę w `docs/spec/<moduł>.md`. Ostrzeżenie, nie blokada.

---

# 6. SZABLONY

## `docs/state/CURRENT.md`

```markdown
# Plaster 2.4 · M-21 Silnik wyceny — rdzeń

**Spec:** docs/spec/quotation.md sekcje 3–5
**Zależy od:** 2.3 (opłaty portowe)
**Moduły dotykane:** M-21, M-17, M-18

## Zakres
Dobór kandydatów na stawki dla zapytania, realizowany w SQL.
Wejście: pol, pod, mode, kontenery, incoterm, ready_date.
Wyjście: lista RateCandidate pogrupowana po dostawcy.

## Poza zakresem
Narzuty (2.6), waluty (2.8), kanały armatorskie (7.7), PDF (2.9).

## Ustalenia
- Data odniesienia: latest_gate_cutoff = ready_date_to + drayage_days
- Dla DG: cutoff_dg zamiast cutoff_gate
- validity_basis rozstrzyga, którą datę porównujemy

## Warunek ukończenia
- [ ] p95 < 300 ms na 50k rate_line (test perf)
- [ ] EXPLAIN pokazuje użycie indeksu pokrywającego
- [ ] Test: wygasła stawka nie trafia do kandydatów
- [ ] Test: izolacja tenantów
```

## `docs/adr/NNNN-tytul.md`

```markdown
# NNNN · Tytuł decyzji

**Status:** przyjęta | zastąpiona przez NNNN
**Data:** RRRR-MM-DD
**Moduły:** M-xx

## Kontekst
Co skłoniło do decyzji. Jakie ograniczenia.

## Decyzja
Co postanowiono. Jednoznacznie.

## Rozważane alternatywy
Co odrzucono i dlaczego. To jest najcenniejsza sekcja za rok.

## Konsekwencje
Co się przez to staje łatwe, co trudne.
```

## `.github/pull_request_template.md`

```markdown
## Plaster
ID: · Moduł: M-xx

## Co się zmienia
Dwa–trzy zdania. Bez listy plików.

## Decyzje
Nietypowe wybory i uzasadnienie. ADR jeśli architektoniczna.

## Wydajność
EXPLAIN ANALYZE dla nowych zapytań do tabel > 10k wierszy.

## Kontrola
- [ ] `just gate` przechodzi
- [ ] Test izolacji tenantów dla nowych tabel
- [ ] `docs/spec/` zaktualizowana
- [ ] Migracja testowana w obie strony
- [ ] Brak nowych ostrzeżeń złożoności
```

---

# 7. `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://localhost/dev"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

**Postgres MCP** eliminuje zgadywanie schematu — największa pojedyncza poprawa
trafności. **Context7** wstrzykuje aktualną dokumentację bibliotek, przez co
agent nie pisze pod wersję sprzed dwóch lat.
