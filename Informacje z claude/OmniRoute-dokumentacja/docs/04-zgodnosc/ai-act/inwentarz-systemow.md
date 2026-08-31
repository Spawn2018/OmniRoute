---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Inwentarz systemów AI

Wymagany do wykazania zgodności z rozporządzeniem o sztucznej inteligencji.

| # | Zastosowanie | Moduł | Klasyfikacja | Uzasadnienie |
|---|---|---|---|---|
| 1 | Ekstrakcja danych z cenników | M-20 | minimalne ryzyko | przetwarzanie dokumentów, decyzja człowieka |
| 2 | Klasyfikacja poczty przychodzącej | M-28 | minimalne ryzyko | kategoryzacja, próg akceptacji |
| 3 | Mapowanie nazw opłat | M-06 | minimalne ryzyko | dopasowanie słownikowe |
| 4 | Personalizacja korespondencji | M-30 | **ograniczone** | art. 50 — obowiązek oznaczenia treści generowanej |
| 5 | Copilot w interfejsie | M-58 | **ograniczone** | art. 50 — obowiązek poinformowania o interakcji z AI |
| 6 | Text-to-SQL w raportach | M-59 | minimalne ryzyko | zapytanie walidowane, brak decyzji |
| 7 | Ocena zdolności kredytowej | M-15 | **wykluczone z wysokiego ryzyka przez ograniczenie zakresu** | punktacja wyłącznie dla osób prawnych; zał. III pkt 5(b) dotyczy osób fizycznych |
| 8 | Wykrywanie oszustw | M-54 | minimalne ryzyko | wykrywanie oszustw wyłączone z zał. III |
| 9 | Prognoza stawek | M-206 | minimalne ryzyko | prognoza rynkowa, bez wpływu na prawa osób |
| 10 | Cyfrowi współpracownicy | M-60 | minimalne ryzyko | bramka akceptacji człowieka przy każdej akcji |

## Wnioski

**Nie prowadzimy systemów wysokiego ryzyka** w rozumieniu załącznika III —
pod warunkiem utrzymania ograniczenia z pozycji 7. To ograniczenie jest
wymuszone kodem i testem, nie polityką.

## Obowiązki, które nas dotyczą

| Obowiązek | Termin | Status |
|---|---|---|
| Kompetencje w zakresie AI (art. 4) | od 2.02.2025 | rejestr szkoleń w M-112 |
| Przejrzystość (art. 50 ust. 1) | od 2.08.2026 | oznaczenie treści generowanej |
| Zakazane praktyki (art. 5) | od 2.02.2025 | nie stosujemy |

## Przegląd

Inwentarz przeglądany przy każdym nowym zastosowaniu modelu językowego
oraz kwartalnie. Nowe zastosowanie wymaga klasyfikacji przed wdrożeniem.
