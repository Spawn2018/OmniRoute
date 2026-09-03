# Oszustwo

Na `/fraud` zapisujesz flagę na kontrahencie — to wskazanie operatora, nie scoring osoby i nie kwota.

1. Zapisz kontrahenta na `/parties`.
2. Wejdź na Oszustwo. Wklej `party_id`, wybierz rodzaj (`billing` / `document` / `other`) i `source_ref` (`fixture://fraud-flag/…` albo `tenant:manual`).
3. „Zapisz flagę” wiąże te wskazania z wierszem `fraud_flag`. Zły rodzaj albo puste źródło odrzuca. Nieznany kontrahent też.
4. Sprawdzenie sankcji zostaje na `/sanctions`. Reklamacja ładunku zostaje na `/claims`. System nie liczy ryzyka.

Czego tu nie ma: scoring osoby, kwota, live lista, auto-match. Marża zostaje na `/charges`.

Nazwy w kodzie: `fraud_flag` · `flag_kind` · `source_ref`.
