# BC terminal_slot_connector (T8)

HITL katalog capability slotu per tenant. connector_code + terminal_code + mode + godziny N4 + source_ref. Nie booking. Nie live T8. Nie confirmed z formularza.

## Dozwolone zależności
- `app.models.terminal_slot_connector`
- `app.repositories.terminal_slot_connectors`
- `app.domain`

## Zakaz
- import innych BC services (dock_appointments, geography, shipments, charges, extraction)
- zapis `dock_appointment` / `terminal` / `shipment` / `charge` / `terminal_appointment`
- live T8 HTTP / Navis N4 / Selenium / kwota / marża / float
- HTTP / slot optimizer / yard
- UPDATE / DELETE wiersza
- kolumna `confirmed` / ustawianie confirmed z POST
