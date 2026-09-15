# BC crm_dedup_mark (BR6.0 leftover)

HITL katalog stance dedup CRM per tenant. mark_code + dedup_kind
nip|vat|email|other + source_ref. Nie merge SQL. Nie cold-send.

## Dozwolone zależności
- `app.models.crm_dedup_mark`
- `app.repositories.crm_dedup_marks`
- `app.domain`

## Zakaz
- import innych BC services (crm_leads, crm_opportunities, crm_activities, crm_pipeline_marks, parties, charges, extraction)
- zapis `crm_lead` / `crm_opportunity` / `crm_activity` / `party` / `quotation` / `charge`
- merge SQL / cold-send / FK lead/opportunity / scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `crm_lead` / `crm_opportunity` / `crm_activity` / `party`
