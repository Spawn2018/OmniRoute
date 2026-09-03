# Różnica kursowa przy wycenie

Kurs NBP przy walutach z opłaty to jeszcze nie różnica kursowa. Wiersz powstaje, gdy go **zapiszesz** na `/fx-differences`.

1. Najpierw zapisz wycenę na `/quotations` i kurs na `/nbp-rates`.
2. Wejdź na Różnice kursowe. Wklej `quotation_id`, `nbp_rate_id` i `source_ref` (`fixture://fx-difference/…` albo `tenant:manual`).
3. „Zapisz różnicę” wiąże te dwa wiersze. System nie mnoży kwot kursem i nie odejmuje kursów.

Czego tu nie ma: kwota na tym wierszu, zysk/strata FX, przeliczenie. Sprzedaż zostaje na `/charges`. Kurs zostaje na `/nbp-rates`.

Nazwy w kodzie: `fx_difference` · `quotation_id` · `nbp_rate_id` · `source_ref`.
