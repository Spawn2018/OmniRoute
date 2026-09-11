# BC lc_checklist (G3)

HITL katalog checklisty LC per tenant. checklist_code + status_kind open|presented|closed|other + source_ref. Nie bank. Nie due.

## Dozwolone zależności
- `app.models.lc_checklist`
- `app.repositories.lc_checklists`
- `app.domain`

## Zakaz
- import innych BC services (document_checklist_rules, parties, charges, extraction)
- zapis `document_checklist_rule` / `party` / `charge`
- bank stakeholder / presentation_due / amount / float / kwota
- HTTP
- UPDATE / DELETE wiersza
