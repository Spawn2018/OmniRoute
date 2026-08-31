---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Reagowanie na incydenty

## Klasyfikacja

| Poziom | Definicja | Reakcja | Zawiadomienie |
|---|---|---|---|
| **P1** | wyciek danych, dostęp międzytenantowy, całkowita niedostępność | 15 min | organ nadzorczy w 72 h, klienci niezwłocznie |
| **P2** | nieuprawniony dostęp bez wycieku, częściowa niedostępność, utrata danych | 1 h | klienci w 24 h |
| **P3** | degradacja, podatność bez dowodu wykorzystania | 4 h | podsumowanie miesięczne |
| **P4** | usterka bez wpływu na dane i dostępność | 1 dzień roboczy | changelog |

## Przebieg

```
WYKRYCIE → OCENA → OGRANICZENIE → USUNIĘCIE → ODTWORZENIE → WNIOSKI
```

**Wykrycie.** Alert automatyczny, zgłoszenie klienta albo obserwacja własna.
Rejestracja w `security_incident` z czasem wykrycia.

**Ocena.** Poziom, zakres, którzy tenanci, ile rekordów, czy dane osobowe.
Przy wątpliwości klasyfikuj wyżej.

**Ograniczenie.** Zatrzymanie rozprzestrzeniania: wyłączenie funkcji,
odcięcie integracji, zablokowanie konta, tryb tylko do odczytu.

**Usunięcie.** Naprawa przyczyny. Przy P1 i P2 nie improwizuj — użyj runbooka.

**Odtworzenie.** Przywrócenie działania, weryfikacja spójności danych.

**Wnioski.** Analiza przyczyny źródłowej w ciągu pięciu dni roboczych.
Bez szukania winnego — szukanie luki w procesie.

## Obowiązki informacyjne

| Zdarzenie | Komu | Termin |
|---|---|---|
| Naruszenie ochrony danych | organ nadzorczy | 72 h od stwierdzenia |
| Naruszenie z wysokim ryzykiem | osoby, których dane dotyczą | niezwłocznie |
| Incydent dotyczący danych klienta | klient | wg umowy, nie później niż 24 h |
| Podatność krytyczna | klienci, jeśli dotyczy ich danych | niezwłocznie |

## Kontakty

| Rola | Osoba | Kontakt |
|---|---|---|
| Osoba odpowiedzialna | Sebastian Bożek | +48 695 637 907 · sebastian@log-mar.pl |
| Zastępstwo | [DO UZUPEŁNIENIA] | — |
| Kancelaria | [DO UZUPEŁNIENIA] | — |
| Ubezpieczyciel OC IT | [DO UZUPEŁNIENIA] | — |
| Hetzner — wsparcie | — | konto klienta |

**Brak zastępstwa jest ryzykiem operacyjnym.** Przy pracy jednoosobowej
warto ustalić choćby osobę, która w razie niedostępności powiadomi klientów.
