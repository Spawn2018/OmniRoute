# T5 task — wpis zadania HITL

**Plaster:** 616.0 HITL katalog. Matching SQL / FK kontekstu / outbox = leftover.
**Status:** fundament (kod + template_code tekst + status + pochodzenie). Nie silnik.

## Zakres

- Tabela `task` per tenant: `task_code` (snake 2–32), `template_code` (snake tekst, nie FK), `status_kind` (`open`|`done`|`skipped`|`other`), `source_ref`
- Unique `(organization_id, task_code)` i `(organization_id, source_ref)`
- OpenFGA `can_manage_tasks` = member
- UI `/tasks`

## Poza zakresem

matching `applies_when` · FK shipment/trip/stop · assignee · outbox / Temporal · M-71 · live HTTP · kwota / marża

## HC

- RLS FORCE + test izolacji
- HC-02: `charge` zostaje prawdą o marży
- TaskService nie importuje `task_templates` / `shipments` / `charges` / `outbox_events`
