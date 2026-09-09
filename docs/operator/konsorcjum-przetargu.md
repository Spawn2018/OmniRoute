# Konsorcjum przetargu

Na `/tender-consortium-members` zapisujesz **fotel** przy istniejącym nagłówku przetargu i kontrahencie. To nie extract RFP i nie TED.

1. Wejdź na Konsorcjum przetargu. Wklej `tender_id` nagłówka i `party_id` kontrahenta tenanta.
2. Wybierz `lead` albo `member`.
3. „Zapisz fotel” z `source_ref` (`fixture://tender-consortium-member/…` albo `tenant:manual`).

Czego tu nie ma: extract RFP, TED live HTTP, auto-award, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`. Kontrahent zostaje na `/parties`.

Nazwy w kodzie: `tender_consortium_member` · `tender_id` · `party_id` · `seat_code` · `source_ref`.
