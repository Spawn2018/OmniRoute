# BC document_kind_match_mark (C8 leftover)

HITL katalog stancji dopasowania rodzaju dokumentu per tenant. mark_code +
match_kind exact|alias|missing|other + source_ref. Nie live matching.
Nie party_document SQL.

## Dozwolone zależności
- `app.models.document_kind_match_mark`
- `app.repositories.document_kind_match_marks`
- `app.domain`

## Zakaz
- import innych BC services (party_documents, relation_document_requirements, create_block_marks, charges)
- zapis `party_document` / `relation_document_requirement` / `create_block_mark` / `charge`
- live matching SQL / 409 / blocks_create egzekucja
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
