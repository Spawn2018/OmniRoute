# BC crm_lead (G1)

HITL katalog leada CRM per tenant. lead_code + stage_kind new|qualified|disqualified|other + source_ref. Nie szansa. Nie cold-send.

## Dozwolone zależności
- `app.models.crm_lead`
- `app.repositories.crm_leads`
- `app.domain`

## Zakaz
- import innych BC services (parties, quotations, charges, extraction)
- zapis `party` / `crm_opportunity` / `charge`
- dedup NIP / cold auto-send / amount / pipeline / float / kwota
- HTTP
- UPDATE / DELETE wiersza
