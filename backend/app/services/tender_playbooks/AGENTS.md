# BC tender_playbook (G2.6)

Playbook per tenant. Twierdzenie + source_ref. Nie extract RFP. Nie kwota.

## Dozwolone zależności
- `app.models.tender_playbook`
- `app.repositories.tender_playbooks`
- `app.domain`

## Zakaz
- import innych BC services (tenders, extraction, charges, quotations)
- zapis `tender` / `extraction_draft` / `charge`
- extract RFP / LLM / kwota / marża / float
- HTTP
