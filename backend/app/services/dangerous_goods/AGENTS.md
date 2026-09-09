# BC dangerous_good (M-52)

Katalog numeru UN + klasy IMDG — nie `charge`. FK na RFQ/wycenie składa API.

## Dozwolone zależności
- `app.models.dangerous_good`
- `app.repositories.dangerous_goods`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `customer_rfq` / `commodity_code` / `charge`
- nadawanie klasy przez LLM
- live IMO / packing group
