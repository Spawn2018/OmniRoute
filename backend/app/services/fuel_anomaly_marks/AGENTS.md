# BC fuel_anomaly_mark (EXP2.14)

HITL katalog znacznika karty/anomalii paliwa per tenant. mark_code + anomaly_kind
card|tank|spike|other + source_ref. Nie live fuel card. Nie telemetry.

## Dozwolone zależności
- `app.models.fuel_anomaly_mark`
- `app.repositories.fuel_anomaly_marks`
- `app.domain`

## Zakaz
- import innych BC services (fuel_indexes, charges, trips, extraction)
- zapis `fuel_index` / `charge` / `trip` / `extraction_draft`
- fuel anomaly live / fuel card HTTP / tank telemetry / mnożenie FSC
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza