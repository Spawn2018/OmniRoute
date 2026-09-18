# BC create_block_mark (C8 leftover)

HITL katalog stancji bramy create per tenant. mark_code + block_kind
block|warn|allow|other + source_ref. Nie live 409. Nie blocks_create egzekucja.

## Dozwolone zależności
- `app.models.create_block_mark`
- `app.repositories.create_block_marks`
- `app.domain`

## Zakaz
- import innych BC services (relation_document_requirements, shipments, parties, charges)
- zapis `shipment` / `relation_document_requirement` / `party_document` / `charge`
- live 409 na POST shipment / blocks_create egzekucja / document_kind matching
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
