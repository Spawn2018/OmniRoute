# BC fuel_index (P3)

Katalog indeksu FSC/BAF/CAF per tenant. Obok `nbp_rate`. Nie mnożenie na `charge`.

## Dozwolone zależności
- `app.models.fuel_index`
- `app.repositories.fuel_indexes`
- `app.domain`

## Zakaz
- import innych BC services (nbp_rates, charges, rate_cards, groupage_tariffs)
- zapis `charge` / `nbp_rate` / `rate_card`
- przeliczenie SQL na `charge`
- float / T-SQL / live HTTP
