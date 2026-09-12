# BC partner_exchange_mark (EXP2.24)

HITL katalog znacznika gieldy partnerskiej per tenant. mark_code + exchange_kind
partner|spot|board|other + source_ref. Nie live Trans.eu. Nie auto-post.
Obok exchange_connectors — tu tryb gieldy, nie konektor.

## Dozwolone zaleznosci
- `app.models.partner_exchange_mark`
- `app.repositories.partner_exchange_marks`
- `app.domain`

## Zakaz
- import innych BC services (exchange_connectors, charges, extraction, networks)
- zapis `exchange_connector` / `charge` / `network` / `extraction_draft`
- Trans.eu / TIMOCOM live / scrape / auto-post
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
