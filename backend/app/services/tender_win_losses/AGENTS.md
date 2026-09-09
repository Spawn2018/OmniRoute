# BC tender_win_loss (G2.7)

Win/loss per tenant. Wynik + source_ref. Nie extract RFP. Nie four-eyes. Nie kwota.

## Dozwolone zależności
- `app.models.tender_win_loss`
- `app.repositories.tender_win_losses`
- `app.domain`

## Zakaz
- import innych BC services (tenders, extraction, charges, quotations, operator_decisions)
- zapis `tender` / `extraction_draft` / `charge`
- extract RFP / LLM / kwota / marża / float / UPDATE `tender.status`
- HTTP
