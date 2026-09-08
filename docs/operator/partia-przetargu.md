# Partia przetargu

Na `/tender-lots` zapisujesz **kod partii** przy istniejącym nagłówku przetargu. To nie korytarz i nie auto-award.

1. Wejdź na Partie przetargu. Wklej `tender_id` nagłówka tenanta.
2. Podaj kod partii (`lot_code`).
3. „Zapisz partię” z `source_ref` (`fixture://tender-lot/…` albo `tenant:manual`).

Czego tu nie ma: korytarz G2.2, auto-award, kwota na tym wierszu. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_lot` · `tender_id` · `lot_code` · `source_ref`.
