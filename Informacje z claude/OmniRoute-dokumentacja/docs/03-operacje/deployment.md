---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Wdrożenia

## Proces

```
merge do main → CI → budowa obrazu → migracja → wdrożenie → weryfikacja
```

Bez okien wydawniczych. Wdrażamy, gdy gotowe.

## Migracje wstecznie zgodne

Zasada trzech kroków, każdy w osobnym wdrożeniu:

```
1. dodaj kolumnę, kod jej nie używa
2. przepnij kod na nową kolumnę
3. usuń starą kolumnę
```

Nigdy w jednej migracji. Dzięki temu wycofanie wdrożenia nie psuje bazy.

## Weryfikacja po wdrożeniu

```
□ sprawdzenie stanu zdrowia usług
□ dymne testy ścieżek krytycznych (Playwright)
□ brak wzrostu błędów w Sentry przez 15 minut
□ czasy odpowiedzi w budżecie
```

## Wycofanie

```bash
# obraz
docker compose up -d --force-recreate app:previous-tag

# migracja, tylko jeśli konieczne
just migrate-down
```

**Migracja usuwająca dane nie jest odwracalna.** Stąd zasada trzech kroków.

## Okna serwisowe

Wymagane wyłącznie przy migracjach zmieniających strukturę dużych tabel
albo przy przenoszeniu tenanta do dedykowanej bazy.

Komunikacja: siedem dni wcześniej, mail plus baner w aplikacji plus wpis
na stronie statusu.

## Kopie zapasowe przed wdrożeniem

Automatyczna kopia przed każdą migracją. Weryfikacja, że kopia się utworzyła,
przed uruchomieniem migracji.
