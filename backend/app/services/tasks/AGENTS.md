# BC task (T5)

HITL katalog wpisu zadania per tenant. task_code + template_code
(tekst, nie FK) + status_kind open|done|skipped|other + source_ref.
Nie matching. Nie FK shipment/trip/stop.

## Dozwolone zależności
- `app.models.task`
- `app.repositories.tasks`
- `app.domain`

## Zakaz
- import innych BC services (task_templates, shipments, trips, charges, outbox_events, extraction)
- zapis `task_template` / `shipment` / `trip` / `charge` / `outbox_event`
- matching SQL / parser AST / assignee / Temporal
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
