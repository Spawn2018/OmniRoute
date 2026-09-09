# BC tender_carbon_mark (G2.14)

HITL znacznik śladu węglowego per tenant. mark_code + source_ref. Nie kg. Nie kalkulator. Nie marża.

## Dozwolone zależności
- `app.models.tender_carbon_mark`
- `app.repositories.tender_carbon_marks`
- `app.domain`

## Zakaz
- import innych BC services (tenders, extraction, charges)
- zapis `tender` / `charge` / `dangerous_good`
- auto-award / kg / mnożenie / LLM / kwota / marża / float
- HTTP
