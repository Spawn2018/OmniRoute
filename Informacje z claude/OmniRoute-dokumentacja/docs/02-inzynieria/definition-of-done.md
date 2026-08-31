---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Definicja ukończenia

Plaster jest ukończony, gdy **wszystkie** poniższe warunki są spełnione.

## Bramka techniczna

```bash
just check      # ruff, mypy, eslint, tsc
just test       # pytest, vitest, pokrycie 80%
just arch       # import-linter: warstwy i granice modułów
just perf       # budżety wydajności
just migrate-down  # migracja w obie strony
just docs       # spec zaktualizowana, OpenAPI wygenerowane
```

## Warunki dodatkowe

```
□ Test izolacji tenantów dla każdej nowej tabeli
□ EXPLAIN ANALYZE w opisie PR dla zapytań do tabel powyżej 10 tys. wierszy
□ Kryteria akceptacji z delta-spec sprawdzone przez subagenta weryfikatora
□ Delta-spec scalona do docs/spec/ i zarchiwizowana
□ ADR utworzony, jeśli zapadła decyzja architektoniczna
□ Wpis w PROGRESS.md
□ Brak nowych ostrzeżeń złożoności i duplikacji
```

## Warunek dla automatyzacji

**Żaden plaster wprowadzający automatyzację nie jest ukończony bez drogi
ręcznej.** Musi istnieć:

```
□ ręczne utworzenie, edycja i usunięcie
□ nadpisanie wartości wyliczonej z uzasadnieniem
□ przycisk „przelicz automatycznie" cofający nadpisanie
□ zapis: kto nadpisał, kiedy, dlaczego, jaka była wartość pierwotna
□ możliwość wyłączenia automatyzacji per tenant
```

## Warunek dla operacji finansowych

```
□ klucz idempotencji
□ przejście przez outbox
□ możliwość storna albo korekty
□ zatwierdzenie powyżej progu
```

## Lista kontrolna przeglądu

Bo intuicja zawodzi w udokumentowany sposób, a autor i recenzent to ta sama
osoba.

```
□ Czy ta logika już gdzieś istnieje?
□ Czy nowa funkcja mogła być rozszerzeniem istniejącej?
□ Czy obsługa błędów jest konkretna, czy maskująca?
□ Czy złożoność którejś funkcji wzrosła o więcej niż 3?
□ Czy testy sprawdzają regułę biznesową, czy implementację?
□ Czy da się to napisać krócej?
□ Jaki to ma wpływ na koszt utrzymania i czas do przychodu?
```
