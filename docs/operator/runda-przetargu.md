# Runda przetargu

Na `/tender-rounds` zapisujesz **numer rundy** przy istniejącym nagłówku przetargu. To nie data room i nie auto-award.

1. Wejdź na Rundy przetargu. Wklej `tender_id` nagłówka tenanta.
2. Podaj numer rundy (`round_no`, liczba ≥ 1).
3. „Zapisz rundę” z `source_ref` (`fixture://tender-round/…` albo `tenant:manual`).

Czego tu nie ma: data room G2.4, auto-award, kwota na tym wierszu. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_round` · `tender_id` · `round_no` · `source_ref`.
