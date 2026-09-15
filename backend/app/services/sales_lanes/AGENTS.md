# BC sales_lane (BR6.1)

HITL katalog korytarza sprzedazy per tenant. lane_code + lane_kind
repeat|spot|other + para UN/LOCODE + source_ref. Nie tender_lane.
Nie lane_pattern. Nie HubSpot.

## Dozwolone zaleznosci
- `app.models.sales_lane`
- `app.repositories.sales_lanes`
- `app.domain`

## Zakaz
- import innych BC services (tender_lanes, lane_patterns, lane_kms, crm_opportunities, charges, extraction)
- zapis `tender_lane` / `lane_pattern` / `lane_km` / `crm_opportunity` / `charge`
- FK do `port` / geography · km / Haversine / HubSpot live
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `tender_lane` / `lane_pattern` / `party` / `quotation`
- kolumna korytarza na `crm_opportunity`
