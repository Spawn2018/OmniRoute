# BC quote_currency_mark (EXP1)

HITL katalog znacznika quote currency per tenant. mark_code + currency_kind
account|pay|other + source_ref. Nie kolumna na quotation. Nie NBP.

## Dozwolone zależności
- `app.models.quote_currency_mark`
- `app.repositories.quote_currency_marks`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, extraction)
- zapis `quotation` / `charge` / `extraction_draft`
- kolumna currency_account/pay / NBP / scoring oferty
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
