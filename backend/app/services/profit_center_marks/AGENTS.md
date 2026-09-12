# BC profit_center_mark (EXP1)

HITL katalog centrum zysku/kosztu/projektu per tenant. mark_code + center_kind
profit|cost|project|other + source_ref. Nie kolumna shipment. Nie kwota.

## Dozwolone zależności
- `app.models.profit_center_mark`
- `app.repositories.profit_center_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, extraction, cost_allocation_marks)
- zapis `shipment` / `charge` / `extraction_draft` / `cost_allocation_mark`
- kolumna profit_center na shipment / ERP live / allocation SQL
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
