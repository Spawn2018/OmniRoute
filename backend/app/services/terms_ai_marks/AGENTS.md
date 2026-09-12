# BC terms_ai_mark (EXP4.15)

HITL katalog znacznika Terms AI per tenant. mark_code + terms_kind
draft|clause|accept|other + source_ref. Nie terms live. Nie CI blob.

## Dozwolone zaleznosci
- `app.models.terms_ai_mark`
- `app.repositories.terms_ai_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction, customer_contracts)
- zapis `customer_contract` / `charge` / `extraction_draft`
- terms live API · CI blob · kwota
- HTTP
- UPDATE / DELETE wiersza
