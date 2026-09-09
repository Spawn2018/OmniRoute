# Ogłoszenie TED

Na `/tender-ted-notices` zapisujesz **numer ogłoszenia TED** przy istniejącym nagłówku przetargu. To nie pobranie z TED.europa.eu i nie auto-award.

1. Wejdź na Ogłoszenie TED. Wklej `tender_id` nagłówka tenanta.
2. Wpisz numer ogłoszenia (np. `123456-2024` albo `2024/S 012-000001`). Nie wklejaj URL.
3. „Zapisz ogłoszenie TED” z `source_ref` (`fixture://tender-ted-notice/…` albo `tenant:manual`).

Czego tu nie ma: scrape TED, live HTTP, zmiana `tender.status`, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`. CO₂ zostaje leftover.

Nazwy w kodzie: `tender_ted_notice` · `tender_id` · `notice_number` · `source_ref`.
