# BC tender_consortium_member (G2.8)

Fotel konsorcjum per tenant. seat_code + source_ref. Nie extract RFP. Nie TED. Nie kwota.

## Dozwolone zależności
- `app.models.tender_consortium_member`
- `app.repositories.tender_consortium_members`
- `app.domain`

## Zakaz
- import innych BC services (tenders, parties, extraction, charges, quotations)
- zapis `tender` / `party` / `extraction_draft` / `charge`
- extract RFP / LLM / kwota / marża / float / TED HTTP
- HTTP
