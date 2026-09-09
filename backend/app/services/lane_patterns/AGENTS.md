# BC lane_pattern (G2.19)

HITL wzorzec korytarza per tenant. Para UN/LOCODE + source_ref. Nie km. Nie circle_sim. Nie marża.

## Dozwolone zależności
- `app.models.lane_pattern`
- `app.repositories.lane_patterns`
- `app.domain`

## Zakaz
- import innych BC services (tenders, tender_lanes, geography, charges, extraction)
- zapis `tender_lane` / `tender` / `charge` / `trip`
- auto-award / km / circle_sim / LLM / kwota / marża / float
- HTTP
