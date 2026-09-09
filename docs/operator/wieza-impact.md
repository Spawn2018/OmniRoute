# Skutek wieży

Na `/tower-impacts` zapisujesz **znacznik etapu łańcucha** tenanta (stock / produkcja / sprzedaż / ebitda oraz status danych umowy). To nie silnik EBITDA i nie karta osoby.

1. Wejdź na Skutek wieży. Wybierz etap (`stock` / `production` / `sales` / `ebitda`) i status umowy (`missing` / `recorded`).
2. Przy `missing` lista pokazuje stały tekst **brak danych umowy**. Nie wczytuje klauzuli SLA.
3. Podaj `source_ref` (`fixture://tower-impact/…` albo `tenant:manual`).
4. „Zapisz skutek wieży”.

Czego tu nie ma: silnik stock→EBITDA, kara SLA, scoring osoby, suma w przeglądarce. Wieża wyjątków zostaje na `/watchtower`. Marża zostaje na `/charges`.

Nazwy w kodzie: `tower_impact` · `chain_stage` · `contract_data_status` · `source_ref`.
