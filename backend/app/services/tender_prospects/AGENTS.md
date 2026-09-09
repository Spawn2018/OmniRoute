# BC tender_prospect (G2.10)

HITL ślad prospectingu per tenant. outreach_code + source_ref. Nie scrape. Nie bid/no-bid. Nie kwota.

## Dozwolone zależności
- `app.models.tender_prospect`
- `app.repositories.tender_prospects`
- `app.domain`

## Zakaz
- import innych BC services (tenders, parties, extraction, charges, quotations)
- zapis `tender` / `party` / `extraction_draft` / `charge`
- scrape kontaktów / TED HTTP / LLM / kwota / marża / float / auto-award
- HTTP
