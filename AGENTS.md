# AGENTS.md

Kontrakt dla agenta kodującego. Zawsze w kontekście. **Limit: 130 linii.**

## Projekt

Wielodostępna platforma spedycyjna. 70 modułów (`M-01`…`M-70`), ~130 obiektów.
Produkt na sprzedaż, wielu tenantów, ruch produkcyjny.

**Stos:** PostgreSQL 16 (+RLS, pgvector, pg_trgm) · FastAPI + granian ·
SQLAlchemy 2.0 · Alembic · Pydantic v2 · Temporal · Hatchet · OpenFGA ·
React 19 (+Compiler) + Vite + TanStack (Router/Query/Form/Table) + shadcn/ui +
Tailwind v4 + PostHog · OpenTelemetry

## Nawigacja

| Potrzebujesz | Gdzie |
|---|---|
| Repozytorium GitHub | `https://github.com/Spawn2018/OmniRoute` |
| Mapa repo, granice modułów | `docs/ARCHITECTURE.md` |
| Rejestr modułów `M-xx` | `docs/MODULES.md` |
| Specyfikacja modułu | `docs/spec/<nazwa>.md` |
| Słownik domenowy PL/EN | `docs/GLOSSARY.md` |
| Twarde ograniczenia domenowe | `GROUNDING.md` |
| Decyzje architektoniczne | `docs/adr/` (0001 Cursor factory, 0002 Frontend 2026) |
| Bieżące zadanie | `docs/state/CURRENT.md` |
| Historia plastrów | `docs/state/PROGRESS.md` |
| Archiwum planów (60+ MD) | `Informacje z claude/` |

**Schemat bazy sprawdzasz przez MCP Postgres.** Nie czytaj wszystkich modeli.

## Trzynaście zasad

Wygrywają z każdą inną sugestią, także z twoją.

1. `organization_id` w każdej tabeli. RLS wymuszany przez bazę.
2. Konfiguracja jest danymi, nie kodem.
3. `charge` to jedyne miejsce prawdy o marży. Kupno i sprzedaż na jednym rekordzie.
4. Model językowy wyciąga dane. Kod je przetwarza. **Model nigdy nie liczy.**
5. Każda stawka ma `source_ref`. Bez pochodzenia rekord nie wchodzi.
6. Stawki niemutowalne. Zmiana to nowy rekord i `superseded_by`.
7. Kwoty jako `Decimal`. Nigdy float. Waluta nierozerwalnie z kwotą.
8. Nic z ekstrakcji nie trafia do bazy bez akceptacji człowieka.
9. Poświadczenia zewnętrzne należą do tenanta, szyfrowane jego kluczem.
10. Wszystko z zewnątrz jest niezaufane.
11. **Nie licz w Pythonie tego, co Postgres policzy z indeksem.**
12. **Żadne zapytanie nie sięga po dane więcej niż jednego tenanta.**
13. **Każde wywołanie zewnętrzne idempotentne. Każde zdarzenie przez outbox.**

## Jak pracujesz

- **Jeden pionowy plaster naraz**: migracja → model → repozytorium → serwis →
  endpoint → test → typ na froncie → komponent. Nie buduj modułu w jednym przebiegu.
- **Plan przed kodem.** Powyżej trzech plików: napisz plan, czekaj na akceptację.
- **Test przed implementacją** dla każdej reguły biznesowej.
- Nie dotykaj plików spoza zakresu. Zgłoś, jeśli to konieczne.
- Po zakończeniu: jedna linia w `PROGRESS.md`, aktualizacja `CURRENT.md`.

## Styl

- Python: `ruff` + `mypy --strict`. Bez `Any` bez uzasadnienia w komentarzu.
- TypeScript: `strict`. Bez `any`. `as` tylko na granicy danych zewnętrznych.
- Nazwy z `GLOSSARY.md`. Domena po angielsku, komunikaty po polsku.
- Funkcja robi jedną rzecz. Powyżej 40 linii — podziel albo uzasadnij.
- Złożoność cyklomatyczna ≤ 10. Powyżej — refaktoryzuj w tym samym commicie.

## Czego nie robisz

- Komentarzy powtarzających kod. Komentarz mówi *dlaczego*, nigdy *co*.
- `try/except Exception` bez konkretnej obsługi.
- Abstrakcji „na przyszłość". Trzecie powtórzenie uzasadnia wyodrębnienie, nie drugie.
- `TODO`, `FIXME`, zaślepek, kodu zakomentowanego.
- Emoji w kodzie i commitach.
- Zmian w zastosowanych migracjach. Nowa migracja, zawsze.
- Zapytań w pętli. N+1 poprawiasz natychmiast.
- Pisania od nowa tego, co jest w `docs/MODULES.md` jako zależność.
- Ładowania kontekstu „na wszelki wypadek". Pytaj zamiast zgadywać.

## Definicja ukończenia

```
just check      # ruff, mypy, eslint, tsc
just test       # pytest, vitest, próg pokrycia 80%
just arch       # import-linter: warstwy i niezależność modułów
just perf       # budżety wydajności
just migrate    # migracja w górę i w dół
just docs       # spec zaktualizowana, OpenAPI wygenerowane
```

Plus test izolacji tenantów dla każdej nowej tabeli. Bez wyjątków.

## Budżety wydajności — warunek ukończenia, nie optymalizacja

| Operacja | Próg |
|---|---|
| Wycena ze stawek w bazie (50k wierszy) | p95 < 300 ms |
| Pierwszy wynik z kanałów armatorskich | < 1 s |
| Endpoint API, mediana | < 150 ms |
| Lista stawek, 50k wierszy, wirtualizacja | p95 < 500 ms |
| LCP aplikacji wewnętrznej | < 1,5 s |
| Rozmiar paczki JS (gzip, początkowa) | < 250 kB |

Przekroczenie blokuje merge.

## Bezpieczeństwo

- Sekrety nigdy w kodzie. `.env` w `.gitignore`, produkcja przez Infisical.
- Każdy endpoint ma jawną deklarację uprawnień. Brak = odmowa.
- Dane wejściowe od zewnętrznych: `llm-guard` przed modelem, `presidio` przed API.
- Zapytania SQL generowane przez model przechodzą przez `sqlglot` przed wykonaniem.
