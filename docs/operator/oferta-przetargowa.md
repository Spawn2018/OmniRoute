# Oferta przetargowa kupna

Na `/tender-quotes` zapisujesz **ważność** i **limit zleceń** przy istniejącej wycenie. To nie obiekt przetargu i nie auto-award.

1. Wejdź na Oferty przetargowe. Wklej `quotation_id` wyceny tenanta.
2. Podaj dzień `valid_until` i dodatni limit orderów (integer, nie kwota).
3. „Zapisz ofertę przetargową” z `source_ref` (`fixture://tender-quote/…` albo `tenant:manual`).

Czego tu nie ma: auto-award, loty G2, kwota na tym wierszu. Marża zostaje na `/charges`. Wycena zostaje na `/quotations`.

Nazwy w kodzie: `tender_quote` · `quotation_id` · `valid_until` · `order_limit` · `source_ref`.
