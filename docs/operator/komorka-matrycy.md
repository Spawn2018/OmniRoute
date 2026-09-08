# Komórka matrycy przetargu

Na `/tender-matrix-cells` wklejasz **kwotę z P** przy istniejącym nagłówku przetargu. To nie mapowanie kolumn przez model językowy i nie druga marża.

1. Wejdź na Komórki matrycy. Wklej `tender_id` nagłówka tenanta.
2. Podaj kod komórki (snake), kwotę dodatnią i walutę ISO. Zero i float odpadają.
3. „Zapisz komórkę” z `source_ref` (`fixture://tender-matrix-cell/…` albo `tenant:manual`).

Czego tu nie ma: extract RFP, playbook, auto-award, suma w przeglądarce, wiązanie wiersza `charge`. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_matrix_cell` · `tender_id` · `cell_code` · `amount` · `currency` · `source_ref`.
