# BC dangerous_good (M-52)

Katalog numeru UN + klasy IMDG — nie `charge`. FK na RFQ/wycenie składa API.
HITL `packing_group` I|II|III (642.0). HITL `marine_pollutant` bool (643.0).
HITL `limited_quantity` bool (644.0). Nie live IMO. Nie LLM klasy.

## Dozwolone zależności
- `app.models.dangerous_good`
- `app.repositories.dangerous_goods`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `customer_rfq` / `commodity_code` / `charge`
- nadawanie klasy przez LLM
- live IMO / grupy zgodności 1.xA / live LQ matching
- UPDATE / DELETE wiersza
