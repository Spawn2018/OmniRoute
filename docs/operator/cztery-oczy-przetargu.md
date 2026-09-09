# Cztery oczy nagrody

Na `/tender-award-reviews` zapisujesz **przegląd czterech oczu** przy istniejącym nagłówku przetargu. To nie auto-award i nie szyna Akceptuj/Zmień/Odrzuć.

1. Wejdź na Cztery oczy nagrody. Wklej `tender_id` nagłówka tenanta.
2. Wybierz `countersign` (drugi podpis) albo `challenge` (zakwestionowanie).
3. „Zapisz przegląd” z `source_ref` (`fixture://tender-award-review/…` albo `tenant:manual`).

Czego tu nie ma: zmiana `tender.status`, zapis `tender_win_loss`, auto-award, dwa konta w tym plasterze, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`. Werdykt po fakcie zostaje na `/tender-win-losses`. Decyzje A/Z/O zostają na `/decisions`.

Nazwy w kodzie: `tender_award_review` · `tender_id` · `review_code` · `source_ref`.
