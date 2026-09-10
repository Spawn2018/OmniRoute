# BC task_template (T5)

HITL katalog szablonu zadania per tenant. template_code + applies_when. Nie instancja. Nie matching.

## Dozwolone zależności
- `app.models.task_template`
- `app.repositories.task_templates`
- `app.domain`

## Zakaz
- import innych BC services (shipments, trips, charges, outbox_events, extraction)
- zapis `task` / `shipment` / `charge` / `outbox_event`
- matching SQL / parser AST / kwota / marża / float
- HTTP / Temporal / worker
