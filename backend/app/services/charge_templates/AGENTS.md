# BC charge_template (P2)

Szablon opłat per tenant: kolekcja `charge_code` + daty jako dane. Nie exclusion, nie marża.

## Dozwolone zależności
- `app.models.charge_template`
- `app.repositories.charge_templates`
- `app.repositories.charge_codes` — odczyt katalogu, nie zapis
- `app.domain`

## Zakaz
- import innych BC services (charges, rate_cards, rate_lines, quotations, charge_codes)
- zapis `charge` / `rate_card` / `rate_line` / `charge_code`
- exclusion GiST / nakładanie daterange
- kwoty / marża / float / T-SQL / HTTP
