# BC make_or_buy_mark (EXP2.2)

HITL katalog znacznika make-or-buy per tenant. mark_code + buy_kind
make|buy|hybrid|other + source_ref. Nie silnik kosztu. Nie allocation.

## Dozwolone zależności
- `app.models.make_or_buy_mark`
- `app.repositories.make_or_buy_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices, extraction)
- zapis `charge` / `sales_invoice` / `extraction_draft`
- silnik make-or-buy / allocation SQL / druga marża
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
