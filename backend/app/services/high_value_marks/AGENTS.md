# BC high_value_mark (EXP1)

HITL katalog protokołu high-value per tenant. mark_code + protocol_kind
high_value|protocol|other + source_ref. Nie kolumna shipment. Nie cargo_value.

## Dozwolone zależności
- `app.models.high_value_mark`
- `app.repositories.high_value_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, extraction, cargo_cover_marks)
- zapis `shipment` / `charge` / `extraction_draft` / `cargo_cover_mark`
- kolumna high_value na shipment / insurance live / cargo_value Decimal
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
