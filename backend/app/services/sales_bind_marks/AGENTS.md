# BC sales_bind_mark (BR6.1 leftover)

HITL katalog stance wiązania korytarza per tenant. mark_code + bind_kind
opportunity|party|other + source_ref. Nie HubSpot live. Nie FK UUID.

## Dozwolone zależności
- `app.models.sales_bind_mark`
- `app.repositories.sales_bind_marks`
- `app.domain`

## Zakaz
- import innych BC services (sales_lanes, crm_opportunities, parties, charges, extraction)
- zapis `sales_lane` / `crm_opportunity` / `party` / `quotation` / `charge`
- HubSpot live / FK UUID / km / Haversine / scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `sales_lane` / `crm_opportunity` / `party`
