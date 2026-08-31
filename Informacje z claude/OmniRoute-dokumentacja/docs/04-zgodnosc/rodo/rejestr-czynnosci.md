---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2027-02-28
---

# Rejestr czynności przetwarzania

**Administrator:** LOGMAR Sp. z o.o., ul. Dąbrowa 173/1, 80-297 Banino
NIP 5833329815 · REGON 381827804 · KRS 0000757498
Reprezentacja: Sebastian Bożek, Prezes Zarządu
Kontakt: sebastian@log-mar.pl · +48 695 637 907

**Inspektor ochrony danych:** niewyznaczony — [zweryfikować obowiązek
z kancelarią przy przekroczeniu skali przetwarzania]

---

## Czynność 1 · Świadczenie usługi OmniRoute

| Element | Treść |
|---|---|
| Rola | administrator wobec danych użytkowników klienta, **procesor** wobec danych w systemie |
| Cel | świadczenie usługi na podstawie umowy |
| Podstawa | art. 6 ust. 1 lit. b — wykonanie umowy |
| Kategorie osób | pracownicy klientów, osoby kontaktowe u kontrahentów klientów |
| Kategorie danych | imię, nazwisko, stanowisko, służbowy mail i telefon, identyfikator, logi aktywności |
| Odbiorcy | podprzetwarzający wg osobnego wykazu |
| Transfer poza EOG | tak — dostawca modelu językowego, na podstawie standardowych klauzul |
| Retencja | czas trwania umowy plus okres karencji, następnie usunięcie |
| Zabezpieczenia | RLS, szyfrowanie, kontrola dostępu, audyt, kopie zapasowe |

## Czynność 2 · Automatyczne pozyskiwanie kontaktów

| Element | Treść |
|---|---|
| Rola | procesor w imieniu klienta |
| Cel | budowa bazy kontaktów kontrahentów z korespondencji |
| Podstawa | uzasadniony interes klienta jako administratora |
| Kategorie osób | pracownicy agentów, przewoźników, armatorów |
| Kategorie danych | imię, nazwisko, stanowisko, mail służbowy, telefon ze stopki |
| Obowiązek informacyjny | link w stopce wysyłanych wiadomości |
| Retencja | 3 lata od ostatniego kontaktu, następnie usunięcie |

## Czynność 3 · Weryfikacja kontrahentów

| Element | Treść |
|---|---|
| Cel | weryfikacja w rejestrach publicznych i listach sankcyjnych |
| Podstawa | obowiązek prawny (sankcje), uzasadniony interes (weryfikacja) |
| Kategorie osób | osoby prowadzące działalność gospodarczą, reprezentanci |
| Źródła | GUS, KRS, RDF, biała lista VAT, VIES, listy sankcyjne UE, ONZ, OFAC, OFSI |
| Retencja | wynik skanowania z wersją listy — 5 lat, wymóg dowodowy |

## Czynność 4 · Ocena zdolności kredytowej

| Element | Treść |
|---|---|
| Cel | ocena ryzyka kredytowego kontrahentów klienta |
| Podstawa | uzasadniony interes klienta |
| **Ograniczenie** | **automatyczna punktacja wyłącznie dla osób prawnych.** Dla osób fizycznych prowadzących działalność: prezentacja danych bez punktacji i bez sugerowanego limitu |
| Uzasadnienie | AI Act, załącznik III pkt 5(b) — uniknięcie klasyfikacji wysokiego ryzyka; art. 22 RODO |
| Decyzja | zawsze przez człowieka, z zapisem uzasadnienia |

## Czynność 5 · Przetwarzanie przez model językowy

| Element | Treść |
|---|---|
| Cel | ekstrakcja danych z cenników i klasyfikacja korespondencji |
| Podstawa | wykonanie umowy |
| **Podprzetwarzanie** | dostawca modelu — **ujawnione w umowie powierzenia** |
| Minimalizacja | `presidio` usuwa dane osobowe przed wysłaniem, gdy nie są konieczne |
| Alternatywa | przełącznik przetwarzania wyłącznie lokalnego na życzenie klienta |
| Dane treningowe | **dane klientów nie są wykorzystywane do trenowania modeli** |

## Czynność 6 · Marketing i sprzedaż

| Element | Treść |
|---|---|
| Cel | kontakt z potencjalnymi klientami |
| Podstawa | uzasadniony interes, zgoda przy komunikacji elektronicznej |
| Retencja | do wycofania zgody albo 2 lata od ostatniego kontaktu |
