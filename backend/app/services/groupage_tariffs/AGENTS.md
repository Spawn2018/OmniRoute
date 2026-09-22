# BC groupage_tariff (D5)

Cennik drobnicy per tenant: próg `chargeable_weight` na strefie, opcjonalne `volume_m3`, kwota Decimal. 625.0 nie liczy progu z objętości. Nie silnik P1.

## Dozwolone zależności
- `app.models.groupage_tariff`
- `app.repositories.groupage_tariffs`
- `app.domain`

## Zakaz
- import innych BC services (geography, charges, rate_lines)
- zapis `location` / `rate_line` / `charge` / `groupage_line`
- matching WHEN/IF / T-SQL / float na kwocie
- liczenie marży / `chargeable_weight`
