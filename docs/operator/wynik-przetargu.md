# Wynik przetargu

Na `/tender-win-losses` zapisujesz **werdykt** przy istniejącym nagłówku przetargu. To nie extract RFP i nie auto-award.

1. Wejdź na Wynik przetargu. Wklej `tender_id` nagłówka tenanta.
2. Wybierz `won` / `lost` / `no_bid` i kod powodu (snake).
3. „Zapisz wynik” z `source_ref` (`fixture://tender-win-loss/…` albo `tenant:manual`).

Czego tu nie ma: extract RFP, four-eyes, zmiana `tender.status`, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_win_loss` · `tender_id` · `outcome` · `reason_code` · `source_ref`.
