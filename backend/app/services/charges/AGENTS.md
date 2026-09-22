# BC charge (M-08)

Jedyny wiersz buy+sell. Marża = `margin(buy, sell)` w domenie. Nie accept HITL.
`charge_sell_in_pln` = odczyt SQL (T7d), nie import `nbp_rates`.

## Dozwolone zależności
- `app.models.charge`
- `app.repositories.charges`
- `app.repositories.charge_codes` — odczyt katalogu, nie zapis
- `app.repositories.rate_lines` — odczyt źródła kupna, nie zapis
- `app.domain`

## Zakaz
- import innych BC services (w tym `nbp_rates`)
- druga tabela / kolumna jako magazyn marży
- float; kurs walutowy w Pythonie
- zapis z `ExtractionService`
