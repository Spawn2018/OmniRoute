# BC margin_floor (N6)

HITL katalog podłogi marży per tenant. floor_code + para UN/LOCODE +
floor_amount Decimal + floor_currency + source_ref. Nie 409 w tym BC.
Egzekucja 409 = compose w API `charges` (539.0). Nie matching lane.

## Dozwolone zależności
- `app.models.margin_floor`
- `app.repositories.margin_floors`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_lanes, rate_cards, extraction)
- zapis `charge` / `sales_lane` / `rate_card` / `extraction_draft`
- 409 / S11 / matching lane w serwisie tego BC
- float
- HTTP
- UPDATE / DELETE wiersza
- FK do charge / sales_lane / quotation
