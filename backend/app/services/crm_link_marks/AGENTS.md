# BC crm_link_mark (BR6.0 leftover)

HITL katalog stance powiązania CRM per tenant. mark_code + link_kind
lead|party|other + source_ref. Nie FK UUID. Nie cold-send.

## Dozwolone zależności
- `app.models.crm_link_mark`
- `app.repositories.crm_link_marks`
- `app.domain`

## Zakaz
- import innych BC services (crm_leads, crm_opportunities, crm_activities, crm_dedup_marks, parties, charges, extraction)
- zapis `crm_lead` / `crm_opportunity` / `crm_activity` / `party` / `quotation` / `charge`
- FK UUID / cold-send / merge SQL / scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `crm_lead` / `crm_opportunity` / `crm_activity` / `party`
