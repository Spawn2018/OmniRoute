# BC tender_decline_reason (EXP3.12)

HITL katalog powodu decline per tenant. mark_code + decline_kind
decline|no_bid|withdraw|other + source_ref. Nie auto-award. Nie RFP scrape.

## Dozwolone zaleznosci
- `app.models.tender_decline_reason`
- `app.repositories.tender_decline_reasons`
- `app.domain`

## Zakaz
- import innych BC services (tenders, charges, extraction)
- zapis `tender` / `charge` / `tender_win_loss`
- decline auto · RFP scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
