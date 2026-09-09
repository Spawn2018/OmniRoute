# Ledger predykcji

Na `/prediction-ledgers` dopisujesz wiersz z przedziałem (minuty) i metryką po fakcie (`crps`, `mae`). To nie wróżba punktowa i nie silnik, który liczy CRPS.

1. Wejdź na Ledger predykcji. Wybierz rodzaj (`eta` / `transit` / `disrupt`) i horyzont (`h1h`…`h7d`).
2. Wpisz przedział, CRPS, MAE, kod modelu (snake) i `source_ref` (`fixture://prediction-ledger/…` albo `tenant:manual`).
3. „Zapisz ledger predykcji”. Ten sam `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: liczenie CRPS w serwisie, champion/challenger, drift, GPS, AIS, scoring osoby, `plan_snapshot`, suma w przeglądarce. Marża zostaje na `/charges`.

Nazwy w kodzie: `prediction_ledger` · `prediction_kind` · `horizon_code` · `crps` · `mae` · `source_ref`.
