---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Strategia testów

## Piramida

```
        ╱╲
       ╱E2E╲          ~20 scenariuszy, tylko ścieżki krytyczne
      ╱──────╲
     ╱ Integr. ╲      ~200, testcontainers, prawdziwy Postgres
    ╱────────────╲
   ╱  Jednostkowe ╲   ~2000, reguły biznesowe, hypothesis
  ╱────────────────╲
 ╱ Statyczne: mypy,  ╲ każdy commit, hooki
╱  ruff, import-linter╲
```

## Co gdzie testujemy

| Warstwa | Co | Czym |
|---|---|---|
| Statyczna | typy, styl, granice modułów | ruff, mypy, import-linter |
| Jednostkowa | reguły biznesowe | pytest + hypothesis |
| Integracyjna | repozytoria, migracje, RLS | testcontainers |
| Kontraktowa | zgodność z OpenAPI, API armatorów | schemathesis, pact |
| End-to-end | ścieżki krytyczne | playwright |
| Wydajnościowa | budżety | pytest-benchmark, k6 |
| Bezpieczeństwa | izolacja, autoryzacja, injection | pytest -m security |
| Promptów | skuteczność ekstrakcji | promptfoo, deepeval |
| Mutacyjna | jakość testów rdzenia | mutmut, tygodniowo |

## Reguły obowiązkowe

**Każda nowa tabela ma test izolacji tenantów.** Bez wyjątków.
Wzorzec w `tests/patterns/tenant_isolation.py`.

**Reguły biznesowe testujemy własnościowo, nie przykładami.** Waga obliczeniowa,
przeliczenia walutowe, kaskada narzutów, koszt finansowania, alokacja kosztu
przejazdu — wszystkie przez `hypothesis`.

**Postgres przez testcontainers.** Nigdy SQLite udający Postgresa.

**Bez mockowania własnego kodu.** Mockujemy wyłącznie granice zewnętrzne.

**Nazwa testu to zdanie opisujące regułę:**
`test_chargeable_weight_uses_higher_of_tonnes_or_cbm`

## Ścieżki krytyczne end-to-end

1. zapytanie mailem → wycena → wysłanie oferty
2. akceptacja oferty → booking → dokumenty
3. faktura → KSeF → płatność → dopasowanie
4. ekstrakcja cennika → kolejka review → stawka → użycie w ofercie
5. trafienie sankcyjne → blokada wystawienia oferty

## Progi

| Metryka | Próg |
|---|---|
| Pokrycie kodu | 80% |
| Wynik mutacyjny dla rdzenia | 70% |
| Skuteczność ekstrakcji | mierzona, publikowana, bez progu blokującego |
| Fałszywe pozytywy klasyfikacji | poniżej 5% |

## Testy niestabilne

Trzy losowe porażki oznaczają automatyczną kwarantannę i zadanie do naprawy.
Test failujący losowo uczy ignorowania czerwonego CI.

## Dane testowe

Fabryki, nie utrwalone pliki. Anonimizacja przy kopiowaniu z produkcji —
`scripts/anonymize_dump.py`. Kopiowanie danych produkcyjnych bez anonimizacji
jest naruszeniem umowy powierzenia, także na własnym komputerze.
