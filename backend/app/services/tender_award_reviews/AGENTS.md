# BC tender_award_review (G2.12)

HITL cztery oczy na nagrodę per tenant. review_code + source_ref. Nie auto-award. Nie win/loss. Nie kwota.

## Dozwolone zależności
- `app.models.tender_award_review`
- `app.repositories.tender_award_reviews`
- `app.domain`

## Zakaz
- import innych BC services (tenders, tender_win_losses, operator_decisions, extraction, charges)
- zapis `tender` / `tender_win_loss` / `operator_decision` / `charge`
- auto-award / TED HTTP / LLM / kwota / marża / float / scrape
- HTTP
