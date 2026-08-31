---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Kopie zapasowe i odtwarzanie

## Parametry

| Parametr | Wartość |
|---|---|
| RPO — dopuszczalna utrata danych | 5 minut |
| RTO — czas odtworzenia | 4 godziny |
| Retencja kopii pełnych | 30 dni |
| Retencja dziennika transakcji | 30 dni, odtwarzanie do punktu w czasie |
| Lokalizacja kopii | inny dostawca niż produkcja |
| Szyfrowanie | tak, klucz przechowywany osobno |

## Mechanizm

`pgbackrest` z kopią pełną raz na dobę i archiwizacją ciągłą dziennika.
Pliki z MinIO kopiowane przez `restic` do niezależnego magazynu.

## Weryfikacja — obowiązkowa

**Kopia, która nie była odtworzona, nie istnieje.**

Cotygodniowe automatyczne odtworzenie na osobnej instancji z weryfikacją:

```sql
backup_verification
  backup_id, verified_at
  restore_duration_seconds
  rows_verified, checksum_match
  status, notes
```

Wynik trafia do centrum zaufania jako data ostatniego udanego testu.

## Procedura odtworzenia

```
1. Ustal moment, do którego odtwarzamy
2. Zatrzymaj aplikację, włącz stronę serwisową
3. pgbackrest restore --type=time --target="..."
4. Uruchom bazę, sprawdź spójność
5. Odtwórz pliki z MinIO dla tego samego momentu
6. Uruchom aplikację w trybie tylko do odczytu
7. Weryfikacja przez zapytania kontrolne
8. Otwarcie zapisu
9. Komunikat do klientów z zakresem utraconych danych
```

## Utrata danych jednego tenanta

Odtworzenie punktowe bez wpływu na pozostałych: odtworzenie do instancji
tymczasowej, eksport danych tenanta, import do produkcji z zachowaniem
identyfikatorów.

**Procedura wymaga przetestowania przed pierwszym klientem.**
