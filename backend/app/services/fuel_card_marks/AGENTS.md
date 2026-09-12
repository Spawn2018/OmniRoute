# BC fuel_card_mark (EXP2.14)

HITL katalog znacznika karty paliwowej per tenant. mark_code + card_kind
fuel|anomaly|other + source_ref. Nie live fuel. Nie litry. Nie anomaly SQL.

## Dozwolone zależności
- `app.models.fuel_card_mark`
- `app.repositories.fuel_card_marks`
- `app.domain`

## Zakaz
- import innych BC services (fuel_anomaly_marks, fuel_indexes, charges, extraction)
- zapis `fuel_anomaly_mark` / `fuel_index` / `charge` / `extraction_draft`
- live fuel card API / litry / amount / anomaly SQL engine
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
