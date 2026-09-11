# BC subcontract_edge_mark (EXP2.6)

HITL katalog krawędzi podwykonawstwa per tenant. mark_code + edge_kind
prime|sub|broker|other + source_ref. Nie graf live. Nie matching SQL.

## Dozwolone zależności
- `app.models.subcontract_edge_mark`
- `app.repositories.subcontract_edge_marks`
- `app.domain`

## Zakaz
- import innych BC services (parties, charges, trips, extraction)
- zapis `party` / `charge` / `trip` / `extraction_draft`
- live subcontract graph / matching SQL
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
