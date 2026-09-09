# BC tender_bid_stance (G2.11)

HITL postawa bid/no-bid per tenant. stance_code + source_ref. Nie win/loss. Nie auto-award. Nie kwota.

## Dozwolone zależności
- `app.models.tender_bid_stance`
- `app.repositories.tender_bid_stances`
- `app.domain`

## Zakaz
- import innych BC services (tenders, tender_win_losses, extraction, charges, quotations)
- zapis `tender` / `tender_win_loss` / `extraction_draft` / `charge`
- auto-award / TED HTTP / LLM / kwota / marża / float / scrape
- HTTP
