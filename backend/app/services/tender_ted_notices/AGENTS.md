# BC tender_ted_notice (G2.13)

HITL numer ogłoszenia TED per tenant. notice_number + source_ref. Nie scrape. Nie live HTTP. Nie kwota.

## Dozwolone zależności
- `app.models.tender_ted_notice`
- `app.repositories.tender_ted_notices`
- `app.domain`

## Zakaz
- import innych BC services (tenders, extraction, charges)
- zapis `tender` / `charge` / `tender_win_loss`
- auto-award / TED HTTP / scrape HTML / LLM / kwota / marża / float
- HTTP
