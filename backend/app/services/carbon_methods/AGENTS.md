# BC carbon_method (C5)

HITL katalog metodyki GLEC/GHG per tenant. method_code + method_version + source_ref. Nie kg. Nie kalkulator. Nie marża.

## Dozwolone zależności
- `app.models.carbon_method`
- `app.repositories.carbon_methods`
- `app.domain`

## Zakaz
- import innych BC services (tenders, shipments, charges, extraction)
- zapis `tender` / `tender_carbon_mark` / `charge` / `shipment`
- kg / tCO2e / mnożenie / LLM / kwota / marża / float
- HTTP
