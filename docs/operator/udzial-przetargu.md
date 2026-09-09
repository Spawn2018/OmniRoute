# Udział w przetargu

Na `/tender-bid-stances` zapisujesz **postawę bid/no-bid** przy istniejącym nagłówku przetargu. To nie wynik win/loss i nie auto-award.

1. Wejdź na Udział w przetargu. Wklej `tender_id` nagłówka tenanta.
2. Wybierz `bid` albo `no_bid`.
3. „Zapisz udział” z `source_ref` (`fixture://tender-bid-stance/…` albo `tenant:manual`).

Czego tu nie ma: zmiana `tender.status`, zapis `tender_win_loss`, four-eyes, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`. Wynik po fakcie zostaje na `/tender-win-losses`.

Nazwy w kodzie: `tender_bid_stance` · `tender_id` · `stance_code` · `source_ref`.
