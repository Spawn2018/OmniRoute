---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2027-02-28
---

# Polityka retencji

Dwa reżimy działające w przeciwnych kierunkach: **obowiązek usunięcia**
z RODO i **obowiązek przechowywania** z przepisów podatkowych, celnych
i przewozowych. Przy kolizji wygrywa obowiązek prawny przechowywania.

| Kategoria | Okres | Podstawa | Po terminie |
|---|---|---|---|
| Dokumenty celne | 5 lat od końca roku | przepisy celne | archiwizacja |
| Faktury i księgi | 5 lat od końca roku podatkowego | ordynacja podatkowa | archiwizacja |
| Dokumenty przewozowe | wg umowy i przedawnienia roszczeń | k.c., CMR | archiwizacja |
| Wyniki skanowania sankcyjnego | 5 lat | wymóg dowodowy | archiwizacja |
| Dane kontaktowe kontrahentów | 3 lata od ostatniego kontaktu | uzasadniony interes | usunięcie |
| Logi aplikacji | 90 dni | bezpieczeństwo | usunięcie |
| Logi dostępu i audyt | 2 lata | bezpieczeństwo, dowodowo | anonimizacja |
| Telemetria promptów | 30 dni | diagnostyka | usunięcie |
| Pliki źródłowe cenników | 12 miesięcy | pochodzenie stawek | usunięcie pliku, zachowanie metadanych |
| Nagrania sesji wsparcia | 30 dni | jakość | usunięcie |
| Dane tenanta po rozwiązaniu umowy | 90 dni karencji | możliwość przywrócenia | usunięcie z zachowaniem obowiązków |

## Blokada usunięcia

Przy toczącym się sporze, reklamacji albo postępowaniu retencja automatyczna
nie usuwa dowodów.

```sql
legal_hold
  entity_type, entity_id, reason, placed_by, placed_at, released_at
```

## Rozdzielenie pliku od metadanych

Plik źródłowy cennika może zawierać dane osobowe. Po okresie retencji plik
jest usuwany, a `source_ref` z hashem, arkuszem, wierszem i kolumną pozostaje.
Pochodzenie stawki zostaje, dane osobowe znikają.

## Realizacja praw osób

| Prawo | Termin | Mechanizm |
|---|---|---|
| Dostęp | 30 dni | eksport danych osoby z systemu |
| Sprostowanie | niezwłocznie | edycja z audytem |
| Usunięcie | 30 dni | usunięcie z wyłączeniem objętych obowiązkiem |
| Ograniczenie | niezwłocznie | flaga blokująca przetwarzanie |
| Przenoszenie | 30 dni | eksport w formacie ustrukturyzowanym |
| Sprzeciw | niezwłocznie | zaprzestanie przetwarzania na uzasadnionym interesie |
