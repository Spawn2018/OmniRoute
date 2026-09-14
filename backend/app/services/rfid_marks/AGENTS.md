# BC rfid_mark (BR1.1)

HITL katalog znacznika RFID per tenant. mark_code + rfid_kind
reader|gate|tag|other + source_ref. Nie live poll. Nie EPC.

## Dozwolone zależności
- `app.models.rfid_mark`
- `app.repositories.rfid_marks`
- `app.domain`

## Zakaz
- import innych BC services (wms_flow_marks, shipment_packages, telematics_devices, charges, extraction)
- zapis `wms_flow_mark` / `shipment_package` / `telematics_device` / `charge`
- live Impinj / Zebra / bramki HTTP · bajty EPC · parowanie z bin/lokalizacją
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
