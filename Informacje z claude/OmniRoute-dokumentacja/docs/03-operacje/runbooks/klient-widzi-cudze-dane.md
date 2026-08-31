---
status: aktualny
owner: Sebastian Bożek
severity: P1
last_review: 2026-08-29
---

# Runbook · Klient zgłasza, że widzi cudze dane

**To jest najpoważniejszy scenariusz w systemie. Nie improwizuj.**

## 1. Natychmiast (pierwsze 15 minut)

```
□ Nie kwestionuj zgłoszenia. Zakładaj, że jest prawdziwe.
□ Poproś o zrzut ekranu z widocznym URL i czasem
□ Ustal correlation_id z logów dla tego użytkownika i czasu
□ WŁĄCZ TRYB TYLKO DO ODCZYTU dla całej aplikacji
□ Utwórz wpis w security_incident, poziom P1
```

## 2. Ograniczenie (do 1 godziny)

```
□ Zidentyfikuj endpoint z logów po correlation_id
□ Sprawdź, czy zapytanie miało ustawiony app.current_org
□ Wyłącz endpoint, jeśli da się to zrobić bez zatrzymania systemu
□ Sprawdź audit_log: kto jeszcze wywołał ten endpoint w ostatnich 30 dniach
□ Ustal listę tenantów, których dane mogły być widoczne
```

## 3. Diagnoza

Najczęstsze przyczyny, w kolejności prawdopodobieństwa:

1. Zapytanie omijające repozytorium — brak kontekstu tenanta
2. Polityka RLS bez `FORCE ROW LEVEL SECURITY`
3. `current_setting('app.current_org', true)` zwracające NULL
4. Cache z kluczem bez `organization_id`
5. Widok materializowany bez filtrowania po tenancie
6. Zapytanie na replice bez ustawionego kontekstu

```sql
-- weryfikacja polityk
SELECT tablename, rowsecurity, forcerowsecurity
FROM pg_tables t
JOIN pg_class c ON c.relname = t.tablename
WHERE schemaname = 'public' AND (NOT rowsecurity OR NOT forcerowsecurity);
```

## 4. Usunięcie

```
□ Poprawka z testem odtwarzającym błąd
□ Test izolacji dla tabeli, której dotyczyło
□ Przegląd wszystkich zapytań w tym module
□ Wdrożenie awaryjne
□ Wyłączenie trybu tylko do odczytu po weryfikacji
```

## 5. Obowiązki informacyjne

```
□ Ocena, czy doszło do naruszenia ochrony danych osobowych
□ Jeśli tak: zgłoszenie do organu nadzorczego w 72 h od stwierdzenia
□ Powiadomienie wszystkich tenantów, których dane mogły być widoczne
□ Powiadomienie osób, których dane dotyczą, jeśli wysokie ryzyko
□ Wpis do rejestru naruszeń
```

**Powiadom klientów, nawet jeśli nie masz pewności, że dane zostały odczytane.**
Ukrycie incydentu tego typu kończy działalność, gdy wyjdzie na jaw.

## 6. Po incydencie

```
□ Analiza przyczyny źródłowej w 5 dni roboczych
□ Test architektoniczny wykluczający powtórzenie klasy błędu
□ Wpis do centrum zaufania
□ Przegląd modelu zagrożeń dla M-01
```
