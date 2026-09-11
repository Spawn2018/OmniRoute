# BC sanctions_mark (EXP2.5)

HITL katalog znacznika listy sankcji per tenant. mark_code + list_kind
ofac|eu|un|other + source_ref. Nie live scrape. Nie screening HTTP.

## Dozwolone zależności
- `app.models.sanctions_mark`
- `app.repositories.sanctions_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, parties, extraction)
- zapis `charge` / `party` / `extraction_draft`
- live sanctions scrape / OFAC HTTP / screening
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
