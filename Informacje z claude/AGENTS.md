# AGENTS.md

Kontrakt dla agenta kodującego. Czytany przy każdej sesji. **Nie przekraczaj 120 linii.**

## Projekt

Wielodostępna platforma spedycyjna: zarządzanie stawkami zakupowymi, ofertowanie,
zlecenia morskie i drogowe. Produkt na sprzedaż, nie narzędzie wewnętrzne.

Stos: PostgreSQL 16 + RLS · FastAPI · SQLAlchemy 2.0 · Alembic · Pydantic v2 ·
procrastinate · React 19 + TypeScript + Vite · TanStack · shadcn/ui · Tailwind

## Gdzie czego szukać

| Potrzebujesz | Plik |
|---|---|
| Mapa repozytorium i granice modułów | `docs/ARCHITECTURE.md` |
| Specyfikacja modułu | `docs/spec/<moduł>.md` |
| Decyzje architektoniczne | `docs/adr/` |
| Stan prac, co dalej | `docs/state/PROGRESS.md` |
| Bieżące zadanie | `docs/state/CURRENT.md` |
| Słownik domenowy | `docs/GLOSSARY.md` |

**Nie zgaduj struktury bazy.** Odpytaj schemat przez MCP Postgres albo przeczytaj
najnowszą migrację w `alembic/versions/`.

## Dziesięć zasad, które wygrywają z każdą inną sugestią

1. `organization_id` w każdej tabeli. RLS wymuszany przez bazę, nie przez kod.
2. Konfiguracja jest danymi, nie kodem. Żadnych reguł biznesowych zaszytych na sztywno.
3. `charge` to jedyne miejsce prawdy o marży. Kupno i sprzedaż na jednym rekordzie.
4. Model językowy wyciąga dane. Kod je przetwarza. **Model nigdy nie liczy.**
5. Każda stawka ma `source_ref`. Bez pochodzenia rekord nie wchodzi do bazy.
6. Stawki są niemutowalne. Zmiana to nowy rekord i `superseded_by`.
7. Kwoty jako `Decimal`/`numeric`. Nigdy float. Waluta nierozerwalnie z kwotą.
8. Nic nie trafia do bazy z ekstrakcji bez akceptacji człowieka.
9. Poświadczenia zewnętrzne należą do tenanta, szyfrowane jego kluczem.
10. Wszystko z zewnątrz jest niezaufane. Waliduj, filtruj, loguj.

## Jak pracujesz

- **Jeden pionowy plaster naraz**: migracja → model → serwis → endpoint → test → UI.
  Nie buduj całego modułu w jednym przebiegu.
- **Najpierw test, potem implementacja** dla reguł biznesowych.
- **Nie zaczynaj kodu bez planu.** Jeśli zadanie ma więcej niż trzy pliki,
  napisz plan i poczekaj na akceptację.
- Po zakończeniu plastra dopisz jedną linię do `docs/state/PROGRESS.md`.
- Nie modyfikuj plików spoza zakresu zadania. Zgłoś, jeśli to konieczne.

## Styl kodu

- Python: `ruff` + `mypy --strict`. Typowanie pełne, bez `Any` bez uzasadnienia.
- TypeScript: `strict: true`. Bez `any`. Bez `as` poza granicami zewnętrznymi.
- Nazwy domenowe po angielsku, komunikaty dla użytkownika po polsku.
- Funkcja robi jedną rzecz. Powyżej 40 linii — uzasadnij albo podziel.

## Czego nie robisz

- **Komentarzy opisujących oczywiste.** `# increment counter` nad `i += 1` to szum.
  Komentarz wyjaśnia *dlaczego*, nigdy *co*.
- `try/except` bez konkretnego wyjątku i bez obsługi. Błąd ma być głośny.
- Abstrakcji „na przyszłość". Trzecie powtórzenie uzasadnia wyodrębnienie, nie drugie.
- `TODO`, `FIXME`, zaślepek. Albo działa, albo nie ma tego w commicie.
- Emoji w kodzie i w commitach.
- Zmiany w migracjach już zastosowanych. Nowa migracja, zawsze.
- Zapytań w pętli. Jeśli widzisz N+1, popraw od razu.
- Pisania własnej implementacji tego, co jest w `docs/ARCHITECTURE.md` jako zależność.

## Definicja ukończenia

Zadanie jest gotowe, gdy wszystko poniżej przechodzi:

```
just check      # ruff + mypy + eslint + tsc
just test       # pytest + vitest, próg pokrycia
just arch       # import-linter: granice modułów
just migrate    # migracja w górę i w dół bez błędu
```

Plus: test izolacji tenantów dla każdej nowej tabeli. Plus: aktualizacja
`docs/spec/<moduł>.md`, jeśli zmieniło się zachowanie.

## Wydajność — budżety obowiązujące od pierwszego dnia

| Operacja | Próg |
|---|---|
| Wycena ze stawek w bazie | p95 < 300 ms |
| Wycena z odpytaniem armatorów | pierwszy wynik < 1 s |
| Lista stawek, 50 tys. wierszy | p95 < 500 ms |
| Endpoint API, mediana | < 150 ms |
| LCP interfejsu | < 1,5 s |

Przekroczenie budżetu to błąd, nie optymalizacja na potem.
