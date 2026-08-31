---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Standardy kodowania

## Zasada nadrzędna

Kod ma wyglądać, jakby napisał go doświadczony programista. Egzekwowane
regułami `.cursor/rules/no-slop.mdc` i `anti-sycophancy.mdc` oraz hookiem
po każdej edycji.

## Python

**Narzędzia:** `ruff` (lint + format) · `mypy --strict` · `uv` · `pytest`

```
E,F,B,BLE,C901,ARG,PLW0621,SLF001,F841,S
```

Reguły dobrane pod pięć najczęstszych zapachów w kodzie agentów: szerokie
przechwytywanie wyjątków, nieużywane zmienne, nieużywane argumenty,
przesłonięte zmienne, dostęp do składowych chronionych.

**Konwencje:**
- typowanie pełne, `Any` wyłącznie z uzasadnieniem w komentarzu
- kwoty jako `Money(Decimal, Currency)`, nigdy gołe liczby w domenie
- daty przez `pendulum`, świadome strefy, bez naiwnych `datetime`
- async przy I/O, bez blokujących wywołań w ścieżce żądania
- wyjątki domenowe w `domain/errors.py`, mapowane na HTTP w jednym miejscu
- funkcja robi jedną rzecz, powyżej 40 linii uzasadnij albo podziel
- złożoność cyklomatyczna do 10, powyżej refaktoryzuj w tym samym commicie

## TypeScript

**Narzędzia:** `eslint` · `tsc --strict` · `prettier` · `vitest`

- bez `any`, `as` wyłącznie na granicy danych zewnętrznych
- typy API generowane przez `openapi-ts`, katalog `api/` tylko do odczytu
- stan serwera wyłącznie przez TanStack Query, bez `useEffect` do pobierania
- komponent poniżej 200 linii, jedna odpowiedzialność
- kwoty przez `<Money/>`, nigdy formatowanie inline
- import z plików zbiorczych zabroniony — psuje tree shaking

## SQL i migracje

- każda tabela: `organization_id`, znaczniki czasu, `created_by`, RLS, audyt
- kwoty `numeric(14,4)` plus `char(3)` waluty obok, zawsze parami
- klucze obce z jawnym `ondelete`, bez kaskad na danych finansowych
- migracja działa w górę i w dół, oba kierunki testowane
- zmiany wstecznie zgodne: dodaj kolumnę, przepnij kod, usuń starą — trzy migracje
- indeksy `CONCURRENTLY` na tabelach z danymi
- uzasadnienie indeksu w komentarzu migracji

## Nazewnictwo

Nazwy domenowe z `docs/GLOSSARY.md`. Domena po angielsku, komunikaty
użytkownika po polsku. Zakazane: `data`, `result`, `temp`, `item`, `obj`,
`handler`, `manager`, `helper`, `utils`.

## Komentarze

Komentarz wyjaśnia **dlaczego**, nigdy **co**.

```python
# NBP tabela A z ostatniego dnia roboczego poprzedzającego —
# wymóg ustawy o VAT przy przeliczaniu faktur walutowych
rate = nbp.rate_for(currency, business_day_before(invoice_date))
```

## Commity

Konwencjonalne, z identyfikatorem plastra i atrybucją agenta.

```
feat(M-21): dobór kandydatów na stawki w SQL [plaster 2.4]

Co-authored-by: Cursor Agent <agent@cursor.sh>
```
