---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Obserwowalność

## Warstwa instrumentacji

OpenTelemetry jako jedyna warstwa. Eksport do Sentry, Grafany i Langfuse.
Nie instrumentujemy trzy razy pod trzy narzędzia.

## Identyfikator korelacji

Każde żądanie dostaje `correlation_id` przekazywany przez wszystkie warstwy:
API, serwis, kolejka, worker, wywołanie zewnętrzne, log, zdarzenie outbox,
odpowiedź do klienta w nagłówku.

Bez tego prześledzenie żądania przez pipeline ekstrakcji jest niemożliwe.

## Co logujemy

| Poziom | Co | Przykład |
|---|---|---|
| ERROR | wyjątek nieobsłużony, awaria integracji | timeout API armatora po trzech próbach |
| WARNING | degradacja, przekroczony próg | wycena bez jednego kanału |
| INFO | zdarzenie biznesowe | oferta wysłana, zlecenie utworzone |
| DEBUG | wyłącznie w trybie diagnostycznym | pełne wejście i wyjście modelu |

Logi strukturalne (`structlog`), zawsze z `organization_id`, `correlation_id`
i identyfikatorem użytkownika.

**Nigdy nie logujemy:** haseł, kluczy API, poświadczeń klientów, pełnych
numerów rachunków, treści dokumentów z danymi osobowymi.

## Co mierzymy

| Kategoria | Metryki |
|---|---|
| Techniczne | czas odpowiedzi p50/p95/p99, błędy, przepustowość, wykorzystanie zasobów |
| Baza | wolne zapytania, blokady, rozmiar, brakujące indeksy |
| Kolejki | głębokość, opóźnienie, nieudane zadania, martwe listy |
| AI | koszt per tenant, opóźnienie, skuteczność ekstrakcji, fałszywe pozytywy |
| Biznesowe | czas do oferty, wskaźnik wygranych, wolumen, kondycja tenanta |
| Bezpieczeństwo | nieudane logowania, sesje impersonacji, działania administracyjne |

## Progi alarmowe

| Warunek | Poziom | Kanał |
|---|---|---|
| Dostępność poniżej 99% w godzinie | krytyczny | telefon |
| p95 powyżej budżetu przez 15 minut | wysoki | push |
| Kolejka rośnie przez 30 minut | wysoki | push |
| Błąd integracji z armatorem trzy razy | średni | mail |
| Koszt AI tenanta powyżej progu | średni | mail |
| Kondycja tenanta spada do „w ryzyku" | niski | raport tygodniowy |

## Diagnostyka

`request_replay` do odtworzenia obliczenia z tymi samymi danymi wejściowymi.
`decision_log` do odpowiedzi, dlaczego system wybrał tę stawkę.
Tryb diagnostyczny per tenant włączany z konsoli na godzinę.
