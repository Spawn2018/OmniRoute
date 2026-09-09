# Ślad węglowy przetargu

Na `/tender-carbon-marks` zapisujesz **znacznik śladu** przy istniejącym nagłówku przetargu. To nie kalkulator kilogramów i nie CBAM.

1. Wejdź na Ślad węglowy przetargu. Wklej `tender_id` nagłówka tenanta.
2. Wybierz `declared` (zadeklarowany) albo `exempt` (zwolniony).
3. „Zapisz znacznik śladu” z `source_ref` (`fixture://tender-carbon-mark/…` albo `tenant:manual`).

Czego tu nie ma: kg, tCO₂e, mnożenie współczynnikiem, zmiana `tender.status`, kwota na tym wierszu, suma w przeglądarce. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`. Kilogramy zostają leftover.

Nazwy w kodzie: `tender_carbon_mark` · `tender_id` · `mark_code` · `source_ref`.
