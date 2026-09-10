# T5 task_template — szablon zadania

**Plaster:** 263.0 HITL katalog. 264.0 outbox `task_template_saved` (skład w API). Instancja `task` / matching SQL / konsument = leftover.
**Status:** fundament (kod + warunek jako dane + pochodzenie + kind outbox). Nie worker.

## Zakres

- Tabela `task_template` per tenant: `template_code` (snake 2–32), `applies_when` (tekst 1–512), `source_ref`
- Unique `(organization_id, template_code)` i `(organization_id, source_ref)`
- POST składa `outbox_event` kind `task_template_saved` (`subject_id` = UUID szablonu, bez FK)
- OpenFGA `can_manage_task_templates` = member
- UI `/task-templates`; lista outbox na `/outbox`

## Poza zakresem

instancja `task` · ewaluacja `applies_when` · konsument / Temporal · live HTTP · kwota / marża

## HC

- RLS FORCE + test izolacji
- HC-02: `charge` zostaje prawdą o marży
- ExtractionService nie importuje `task_templates`
- OutboxEventService nie importuje `task_templates`; TaskTemplateService nie importuje outbox
