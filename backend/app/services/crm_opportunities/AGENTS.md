# BC crm_opportunity (BR6.0)

HITL katalog okazji CRM per tenant. opportunity_code + stage_kind
open|won|lost|other + source_ref. Nie pipeline. Nie activity.

## Dozwolone zależności
- `app.models.crm_opportunity`
- `app.repositories.crm_opportunities`
- `app.domain`

## Zakaz
- import innych BC services (crm_leads, funnel_marks, parties, charges, extraction)
- zapis `crm_lead` / `party` / `quotation` / `charge` / `funnel_mark`
- pipeline silnik / activity / cold-send / dedup NIP
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `crm_lead` / `party`
