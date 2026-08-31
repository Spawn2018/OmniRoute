---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2027-02-28
---

# Polityka bezpieczeństwa informacji

**Podmiot:** LOGMAR Sp. z o.o. · **Produkt:** OmniRoute
**Odpowiedzialny:** Sebastian Bożek, Prezes Zarządu

## Zakres

Dotyczy systemu OmniRoute, infrastruktury, procesu wytwarzania i danych
klientów.

## Zasady naczelne

1. **Najmniejsze uprawnienia.** Każdy dostęp uzasadniony i ograniczony.
2. **Obrona wielowarstwowa.** Pojedyncza awaria nie prowadzi do naruszenia.
3. **Bezpieczne domyślnie.** Brak deklaracji uprawnień oznacza odmowę.
4. **Wszystko z zewnątrz niezaufane.** Walidacja, filtracja, logowanie.
5. **Audytowalność.** Każde działanie na danych klienta pozostawia ślad.

## Kontrola dostępu

| Powierzchnia | Uwierzytelnianie | Dwuskładnikowe |
|---|---|---|
| Aplikacja | OIDC | opcjonalne, wymuszalne przez tenanta |
| Konsola administratora | OIDC + osobna domena + ograniczenie IP | **obowiązkowe** |
| Infrastruktura | klucz SSH | **obowiązkowe** |
| API | klucz z zakresem i limitem | — |

Przegląd uprawnień: kwartalnie. Odebranie dostępu: natychmiast po ustaniu
podstawy.

## Ochrona danych

| Zakres | Mechanizm |
|---|---|
| W transporcie | TLS 1.3, HSTS |
| W spoczynku | szyfrowanie wolumenu AES-256 |
| Poświadczenia klientów | szyfrowanie kluczem per tenant |
| Sekrety | Infisical, rotacja kwartalna |
| Kopie zapasowe | szyfrowane, klucz osobno |
| Izolacja tenantów | RLS wymuszany przez bazę, testowany |

## Bezpieczeństwo wytwarzania

Skanowanie na czterech poziomach: sekrety przy edycji i commicie, analiza
statyczna i zależności w CI, kontenery i infrastruktura przed wdrożeniem,
testy dynamiczne nocnie.

Testy penetracyjne: raz w roku przez podmiot zewnętrzny,
pierwszy przed pozyskaniem trzeciego klienta.

## Zarządzanie podatnościami

| Waga | Naprawa |
|---|---|
| Krytyczna | 24 godziny |
| Wysoka | 7 dni |
| Średnia | 30 dni |
| Niska | 90 dni |

Zgłaszanie zewnętrzne: `security@` z polityką ujawniania i deklaracją
niepodejmowania kroków prawnych wobec badaczy działających w dobrej wierze.

## Ciągłość działania

RPO 5 minut, RTO 4 godziny. Cotygodniowa weryfikacja odtworzenia kopii.

## Incydenty

Klasyfikacja P1–P4, procedura w `03-operacje/incident-response.md`.
Zgłoszenie naruszenia ochrony danych do organu nadzorczego w 72 godziny.

## Szkolenia

Przy pracy jednoosobowej: coroczna aktualizacja wiedzy z zakresu
bezpieczeństwa aplikacji webowych i przepisów o ochronie danych.
Przy zatrudnieniu: szkolenie przed nadaniem dostępów.
