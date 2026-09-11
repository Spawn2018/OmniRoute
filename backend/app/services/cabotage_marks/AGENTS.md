# BC cabotage_mark (EXP2.11)

HITL katalog znacznika kabotażu per tenant. mark_code + cabotage_kind
counter|driver_return|vehicle_return|other + source_ref. Nie silnik. Nie RTPD.

## Dozwolone zależności
- `app.models.cabotage_mark`
- `app.repositories.cabotage_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, resources, charges, extraction)
- zapis `trip` / `resource` / `charge` / `extraction_draft`
- cabotage live / RTPD / tacho / licznik SQL
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza