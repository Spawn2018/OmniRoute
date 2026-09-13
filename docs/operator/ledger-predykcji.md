# Ledger predykcji

Na `/prediction-ledgers` dopisujesz wiersz z przedziałem (minuty) i kodem modelu.
To nie wróżba punktowa i nie miejsce na wpisane CRPS ani MAE.

1. Wejdź na Ledger predykcji. Wybierz rodzaj (`eta` / `transit` / `disrupt`) i horyzont (`h1h`…`h7d`).
2. Wpisz przedział, kod modelu (snake) i `source_ref` (`fixture://prediction-ledger/…` albo `tenant:manual`).
3. „Zapisz ledger predykcji”. Ten sam `source_ref` u tenanta nie wejdzie drugi raz.

Liczone CRPS i MAE są na wyniku przedziału (`/interval-scores`), gdy jest
sparowany fakt z ledgeru wyniku. Stare wiersze z wpisaną metryką zostają
w historii — nowego wpisu nie dodasz.

Czego tu nie ma: liczenie CRPS w serwisie, champion/challenger, drift, GPS, AIS, scoring osoby, `plan_snapshot`, suma w przeglądarce. Marża zostaje na `/charges`.

Nazwy w kodzie: `prediction_ledger` · `prediction_kind` · `horizon_code` · `source_ref`.
