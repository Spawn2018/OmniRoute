# product_ticket_mark (Plat-HD)

Katalog znacznika ticketu produktu per tenant. HITL report / triage /
owner_ok. Nie CAPA. Nie auto-naprawa. Nie operator_notice.

- RLS FORCE. OpenFGA `can_manage_product_ticket_marks` = member
- `ticket_kind`: `report` / `triage` / `owner_ok` / `other`
- Unique `(organization_id, mark_code)` i `(organization_id, source_ref)`
- Job: `/product-ticket-marks`

Delta: [480.0](../deltas/open/480.0.md) (po zamknięciu → archived).
