# Prospekt przetargu

Na `/tender-prospects` zapisujesz **ślad outreach** przy istniejącym nagłówku przetargu i kontrahencie. To nie scrape kontaktów i nie silnik bid/no-bid.

1. Wejdź na Prospekt przetargu. Wklej `tender_id` nagłówka i `party_id` kontrahenta tenanta.
2. Wpisz `outreach_code` (snake 2–32, np. `called`).
3. „Zapisz prospekt” z `source_ref` (`fixture://tender-prospect/…` albo `tenant:manual`).

Czego tu nie ma: scrape, TED live HTTP, auto-award, bid/no-bid, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`. Kontrahent zostaje na `/parties`.

Nazwy w kodzie: `tender_prospect` · `tender_id` · `party_id` · `outreach_code` · `source_ref`.
