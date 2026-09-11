# BC otif_mark (CT3)

HITL katalog zakresu OTIF per tenant. mark_code + scope_kind pickup|delivery|sku + source_ref. Nie OTIF%. Nie scoring SQL.

## Dozwolone zależności
- `app.models.otif_mark`
- `app.repositories.otif_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, stops, purchase_orders, charges, extraction)
- zapis `shipment` / `stop` / `po_line` / `charge`
- OTIF% / float / marża / SQL scoring
- HTTP
- UPDATE / DELETE wiersza
