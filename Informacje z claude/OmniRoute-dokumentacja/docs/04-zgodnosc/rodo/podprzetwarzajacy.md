---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Wykaz podprzetwarzających

Dokument publiczny, dostępny dla klientów. Aktualizowany przy każdej zmianie,
z 30-dniowym uprzedzeniem przed dodaniem nowego podmiotu.

| Podmiot | Rola | Lokalizacja | Dane | Podstawa transferu |
|---|---|---|---|---|
| Hetzner Online GmbH | hosting, kopie zapasowe | Niemcy | wszystkie dane systemu | EOG |
| Anthropic | model językowy — ekstrakcja, klasyfikacja | USA | treść cenników, korespondencji | standardowe klauzule umowne |
| Sentry | monitoring błędów | [zweryfikować region] | identyfikatory, ślady błędów | — |
| PostHog | analityka produktowa | [zweryfikować region] | zdarzenia użycia, identyfikatory | — |
| Langfuse | telemetria promptów | [zweryfikować region] | treść promptów i odpowiedzi | — |
| Cloudflare | DNS, ochrona | globalnie | metadane ruchu | standardowe klauzule |
| [Partner faktoringowy] | finansowanie należności | Polska | dane faktur i kontrahentów | umowa powierzenia |
| [Dostawca AIS/PIS] | dostęp do rachunków | Polska | dane transakcji bankowych | umowa powierzenia |

## Zasady

**Zmiana podprzetwarzającego** wymaga powiadomienia klientów z 30-dniowym
wyprzedzeniem. Klient ma prawo sprzeciwu; przy sprzeciwie strony ustalają
rozwiązanie albo umowa może zostać rozwiązana.

**Przetwarzanie wyłącznie lokalne.** Na życzenie klienta możliwe wyłączenie
przetwarzania przez model językowy — funkcje ekstrakcji działają wtedy
w trybie ograniczonym, na modelu uruchomionym lokalnie.

**Weryfikacja.** Każdy podprzetwarzający raz do roku sprawdzany pod kątem
zabezpieczeń i aktualności umowy.
