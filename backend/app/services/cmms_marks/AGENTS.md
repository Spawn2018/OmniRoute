# BC cmms_mark (G7)

HITL katalog znacznika CMMS per tenant. mark_code + work_kind work_order|dtc|other + source_ref. Nie work_order. Nie kwota.

## Dozwolone zależności
- `app.models.cmms_mark`
- `app.repositories.cmms_marks`
- `app.domain`

## Zakaz
- import innych BC services (telematics_connectors, resources, charges, extraction)
- zapis `resource` / `charge` / `telematics_connector` / `trip`
- work_order silnik / dtc z V5 live / kara kierowcy / amount / penalty / float / kwota
- HTTP
- UPDATE / DELETE wiersza
