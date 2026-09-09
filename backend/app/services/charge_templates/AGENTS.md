# BC charge_template (P2)

Szablon opłat per tenant: kolekcja `charge_code` + daty jako dane.
Nakładanie okien liczy Postgres (exclusion). Nie marża.

## Dozwolone zależności
- `app.models.charge_template`
- `app.repositories.charge_templates`
- `app.repositories.charge_codes` — odczyt katalogu, nie zapis
- `app.domain`

## Zakaz
- import innych BC services (charges, rate_cards, rate_lines, quotations, charge_codes, geography)
- zapis `charge` / `rate_card` / `rate_line` / `charge_code`
- porównywanie okien dat w Pythonie
- kwoty / marża / float / T-SQL / HTTP
