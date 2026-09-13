# BC campaign_mark (BR6.5)

HITL katalog znacznika kampanii per tenant. mark_code + campaign_kind
campaign|attribution|other + source_ref. Nie funnel_mark. Nie atrybucja live.

## Dozwolone zaleznosci
- `app.models.campaign_mark`
- `app.repositories.campaign_marks`
- `app.domain`

## Zakaz
- import innych BC services (funnel_marks, crm_opportunities, charges, extraction)
- zapis `funnel_mark` / `crm_opportunity` / `charge`
- atrybucja live / kampania HTTP / lejek silnik
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `funnel_mark` / `crm_opportunity` / `party`
