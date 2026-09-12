# BC mail_accept_mark (EXP4.16)

HITL katalog znacznika Accept z maila per tenant. mark_code + accept_kind
draft|clause|accept|other + source_ref. Nie Graph live. Nie auto-send.

## Dozwolone zaleznosci
- `app.models.mail_accept_mark`
- `app.repositories.mail_accept_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction, customer_contracts)
- zapis `customer_contract` / `charge` / `extraction_draft`
- Graph live API · auto-send · kwota
- HTTP
- UPDATE / DELETE wiersza
