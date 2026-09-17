# BC invoice_match_candidate (F10 leftover)

HITL katalog stancji kandydata dopasowania FV per tenant. candidate_code +
candidate_kind proposed|held|rejected|other + source_ref. Nie ranking SQL.
Nie auto-link.

## Dozwolone zależności
- `app.models.invoice_match_candidate`
- `app.repositories.invoice_match_candidates`
- `app.domain`

## Zakaz
- import innych BC services (invoice_match_marks, purchase_invoices, charges, extraction)
- zapis `invoice_match_mark` / `purchase_invoice` / `charge` / `extraction_draft`
- ranking SQL / score / auto-link
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
