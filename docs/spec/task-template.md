# T5 task_template — szablon zadania

**Plaster:** 263.0 HITL katalog. Instancja `task` / matching SQL / outbox = leftover.
**Status:** fundament (kod + warunek jako dane + pochodzenie). Nie worker.

## Zakres

- Tabela `task_template` per tenant: `template_code` (snake 2–32), `applies_when` (tekst 1–512), `source_ref`
- Unique `(organization_id, template_code)` i `(organization_id, source_ref)`
- OpenFGA `can_manage_task_templates` = member
- UI `/task-templates`

## Poza zakresem

instancja `task` · ewaluacja `applies_when` · outbox / Temporal · live HTTP · kwota / marża

## HC

- RLS FORCE + test izolacji
- HC-02: `charge` zostaje prawdą o marży
- ExtractionService nie importuje `task_templates`
