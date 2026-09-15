# BC crm_pipeline_mark (BR6.0 leftover)

HITL katalog etapu CRM per tenant. mark_code + pipeline_kind
stage|won|lost|hold|other + source_ref. Nie silnik lejka. Nie FK okazji.

## Dozwolone zależności
- `app.models.crm_pipeline_mark`
- `app.repositories.crm_pipeline_marks`
- `app.domain`

## Zakaz
- import innych BC services (crm_leads, crm_opportunities, crm_activities, funnel_marks, parties, charges, extraction)
- zapis `crm_lead` / `crm_opportunity` / `crm_activity` / `party` / `quotation` / `charge` / `funnel_mark`
- silnik lejka / FK okazji / cold-send / dedup NIP
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `crm_lead` / `crm_opportunity` / `crm_activity` / `party`
