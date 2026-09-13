# BC silk_corridor_mark (BR4.4)

HITL katalog znacznika Jedwabnego Szlaku per tenant. mark_code + corridor_kind
silk|block_train|transit|other + source_ref. Nie live CR Express. Nie lane_pattern.

## Dozwolone zależności
- `app.models.silk_corridor_mark`
- `app.repositories.silk_corridor_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipment_legs, lane_patterns, lane_kms, sales_lanes, charges, extraction)
- zapis `shipment_leg` / `lane_pattern` / `lane_km` / `charge` / `extraction_draft`
- live CR Express / China Railway HTTP · km / Haversine · para UN/LOCODE
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
