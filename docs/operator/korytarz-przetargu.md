# Korytarz przetargu

Na `/tender-lanes` zapisujesz **parę UN/LOCODE** przy istniejącej partii. To nie runda i nie auto-award.

1. Wejdź na Korytarze przetargu. Wklej `tender_lot_id` partii tenanta.
2. Podaj origin i destination (pięć znaków, np. PLGDY / DEHAM). Te same końce są odrzucane.
3. „Zapisz korytarz” z `source_ref` (`fixture://tender-lane/…` albo `tenant:manual`).

Czego tu nie ma: runda G2.3, resolve katalogu portów, auto-award, kwota na tym wierszu. Marża zostaje na `/charges`. Partia zostaje na `/tender-lots`.

Nazwy w kodzie: `tender_lane` · `tender_lot_id` · `origin_unlocode` · `destination_unlocode` · `source_ref`.
