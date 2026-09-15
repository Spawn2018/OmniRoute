# BC cost_category_mark (AI7.0 leftover)

HITL katalog kategorii kosztu per tenant. mark_code + category_kind
direct|shared|allocated|overhead|capital|risk|other + source_ref. Nie allocation SQL. Nie TCM.

## Dozwolone zależności
- `app.models.cost_category_mark`
- `app.repositories.cost_category_marks`
- `app.domain`

## Zakaz
- import innych BC services (cost_allocation_marks, allocation_keys, charges, extraction)
- zapis `cost_allocation_mark` / `allocation_key` / `charge` / `extraction_draft`
- allocation SQL / TRUE CONTRIBUTION MARGIN / druga marża
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
