# BC document_checklist_rule (U5)

Reguła checklisty dokumentów per tenant: trójka incoterm × trade_side × mode.
`blocks_dispatch` jest daną. Nie egzekucja dispatch. Nie C8.

## Dozwolone zależności
- `app.models.document_checklist_rule`
- `app.repositories.document_checklist_rules`
- `app.domain`

## Zakaz
- import innych BC services (shipments, shipment_documents, charges)
- zapis `shipment` / `shipment_document` / `charge`
- kwoty / marża / float / dni robocze
- HTTP / parser
