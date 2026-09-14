# BC product_ticket_mark (Plat-HD)

HITL katalog ticketu produktu per tenant. mark_code +
ticket_kind report|triage|owner_ok|other + source_ref. Nie CAPA. Nie auto-naprawa. Nie operator_notice.

## Dozwolone zależności
- `app.models.product_ticket_mark`
- `app.repositories.product_ticket_marks`
- `app.domain`

## Zakaz
- import innych BC services (capa_marks, operator_notices, repair_playbooks, charges, extraction)
- zapis `capa_mark` / `operator_notice` / `repair_playbook` / `charge`
- CAPA · auto-naprawa · operator_notice · Expo Mob
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
