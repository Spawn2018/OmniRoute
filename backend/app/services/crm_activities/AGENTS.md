# BC crm_activity (BR6.0 leftover)

HITL katalog aktywności CRM per tenant. activity_code + activity_kind
call|meeting|email|note|other + source_ref. Nie pipeline. Nie FK okazji.

## Dozwolone zależności
- `app.models.crm_activity`
- `app.repositories.crm_activities`
- `app.domain`

## Zakaz
- import innych BC services (crm_leads, crm_opportunities, funnel_marks, parties, charges, extraction)
- zapis `crm_lead` / `crm_opportunity` / `party` / `quotation` / `charge` / `funnel_mark`
- pipeline silnik / FK okazji / cold-send / dedup NIP
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `crm_lead` / `crm_opportunity` / `party`
