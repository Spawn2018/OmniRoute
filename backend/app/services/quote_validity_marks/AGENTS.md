# BC quote_validity_mark (EXP1)

HITL katalog znacznika quote validity per tenant. mark_code + validity_kind
open|revised|superseded|other + source_ref. Nie kolumna na quotation. Nie data.

## Dozwolone zależności
- `app.models.quote_validity_mark`
- `app.repositories.quote_validity_marks`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, extraction, tender_quotes)
- zapis `quotation` / `charge` / `extraction_draft` / `tender_quote`
- kolumna valid_until/revision_no/supersedes_id / NBP / scoring oferty
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
