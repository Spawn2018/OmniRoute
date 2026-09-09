# Wzorzec korytarza

Na `/lane-patterns` zapisujesz **parę UN/LOCODE** jako wzorzec korytarza tenanta. To nie korytarz partii przetargu i nie silnik km.

1. Wejdź na Wzorzec korytarza. Podaj origin i destination (pięć znaków, np. PLGDY / DEHAM).
2. Te same końce są odrzucane.
3. „Zapisz wzorzec korytarza” z `source_ref` (`fixture://lane-pattern/…` albo `tenant:manual`).

Czego tu nie ma: `tender_lane`, `circle_sim`, km ładowny/pusty/dolot, P z actuals, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Partia zostaje na `/tender-lots`. Korytarz partii zostaje na `/tender-lanes`.

Nazwy w kodzie: `lane_pattern` · `origin_unlocode` · `destination_unlocode` · `source_ref`.
