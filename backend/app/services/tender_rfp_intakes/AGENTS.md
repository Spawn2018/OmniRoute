# BC tender_rfp_intake (G2.9)

HITL przyjęcie RFP per tenant. intake_code + source_ref. Nie zapis z LLM. Nie auto-award.

## Dozwolone zależności
- `app.models.tender_rfp_intake`
- `app.repositories.tender_rfp_intakes`
- `app.domain`

## Zakaz
- import innych BC services (tenders, extraction, charges, quotations)
- zapis `tender` / `extraction_draft` / `charge`
- extract RFP z LLM / auto-award / kwota / marża / float / TED HTTP
- HTTP
