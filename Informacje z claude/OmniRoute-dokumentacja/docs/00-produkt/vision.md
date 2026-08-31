---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# OmniRoute — wizja produktu

## Problem

Spedytor morski traci dwie do trzech godzin dziennie na czynności, które nie
wymagają jego wiedzy: przepisywanie cenników z Excela i PDF, szukanie stawek
w skrzynce, dopytywanie agentów, liczenie ofert w arkuszu.

Skutki mierzalne:
- czas do oferty liczony w godzinach albo dobach, gdy decyduje szybkość
- pominięte dopłaty odkrywane dopiero na fakturze
- brak wiedzy o rzeczywistej rentowności klienta, relacji i agenta
- rozrzut cenowy tej samej usługi sięgający kilkudziesięciu procent

## Dla kogo

Spedytor morski z własną bazą stawek zakupowych i co najmniej dwiema osobami
w ofertowaniu. Polska i rynki ościenne.

Nie budujemy dla: przewoźników drogowych bez spedycji, operatorów magazynowych,
firm kurierskich, korporacji z wdrożonym systemem klasy CargoWise.

## Co robimy

1. **Automatyczna baza cen zakupowych** — cennik z maila, Excela albo PDF jest
   w systemie po minucie, ze śladem pochodzenia do komórki źródłowej.
2. **Kanałowa integracja z armatorami** — API u największych, agregator
   u średnich, automatyczna korespondencja u reszty świata.
3. **Zamknięta pętla** — od maila klienta przez zapytanie do agentów, ofertę,
   zlecenie, fakturę, aż po rozliczenie rozbieżności i koszt kapitału.

## Czego świadomie nie robimy

Pełnej księgowości (integrujemy) · magazynu klasy WMS (tylko CFS) · agencji
morskiej, czarterowania, ładunków projektowych · benchmarku rynkowego z danych
klientów (wykluczone architektonicznie i prawnie).

## Kolejność rynków

| Okres | Gałąź |
|---|---|
| 2026/27 | fracht morski, FCL i LCL |
| 2027 | transport drogowy: drobnica, całopojazdowy, doładunki |
| 2028 | fracht lotniczy |

## Miara sukcesu

| Horyzont | Cel |
|---|---|
| Faza 2 | trzech spedytorów po demo pyta o termin dostępności |
| 12 miesięcy | pięciu płacących klientów |
| 24 miesiące | dwudziestu klientów, przychód powyżej 500 tys. zł rocznie |

**Miara operacyjna, która decyduje o wszystkim:** mediana czasu od zapytania
klienta do wysłanej oferty, mierzona przed wdrożeniem i po.
