# Pokój danych przetargu

Na `/tender-data-rooms` zapisujesz **znacznik NDA** przy istniejącym nagłówku przetargu. To nie extract RFP i nie auto-award.

1. Wejdź na Pokoje danych. Wklej `tender_id` nagłówka tenanta.
2. Zostaw znacznik `signed` (jedyna dozwolona wartość).
3. „Zapisz pokój” z `source_ref` (`fixture://tender-data-room/…` albo `tenant:manual`).

Czego tu nie ma: bajty plików, extract RFP, matryca, auto-award, kwota na tym wierszu. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_data_room` · `tender_id` · `nda_mark` · `source_ref`.
