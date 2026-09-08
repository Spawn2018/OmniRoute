# BC rate_card (P1)

Karta stawek per tenant: `applies_when` jako dane + Decimal. Nie matching, nie T-SQL.

## Dozwolone zależności
- `app.models.rate_card`
- `app.repositories.rate_cards`
- `app.domain`

## Zakaz
- import innych BC services (port_surcharges, rate_lines, charges, groupage_tariffs)
- zapis `charge` / `rate_line` / `port_surcharge`
- matching WHEN/IF / parser AST
- float / T-SQL / HTTP
