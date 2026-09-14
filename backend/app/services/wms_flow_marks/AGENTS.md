# BC wms_flow_mark (BR1.0)

HITL katalog przepływu WMS per tenant. mark_code + flow_kind
receipt|location|pick|ship|count|other + source_ref. Nie live WMS. Nie qty.

## Dozwolone zależności
- `app.models.wms_flow_mark`
- `app.repositories.wms_flow_marks`
- `app.domain`

## Zakaz
- import innych BC services (inventory_position_marks, dock_appointments, purchase_orders, charges, extraction)
- zapis `inventory_position_mark` / `dock_appointment` / `purchase_order` / `charge`
- live Manhattan / SAP EWM / Infios HTTP · RFID · qty float · lokalizacja bin FK
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
