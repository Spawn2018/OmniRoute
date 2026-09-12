# BC slot_guarantee_mark (EXP0.3)

HITL katalog znacznika stance slotu per tenant. mark_code + stance_kind
capability|non_guarantee|other + source_ref. Nie live T8. Nie confirmed.

## Dozwolone zależności
- `app.models.slot_guarantee_mark`
- `app.repositories.slot_guarantee_marks`
- `app.domain`

## Zakaz
- import innych BC services (terminal_slot_connectors, dock_appointments, charges, extraction)
- zapis `terminal_slot_connector` / `dock_appointment` / `charge` / `extraction_draft`
- live T8 / confirmed z POST / yard / slot optimizer
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
