# BC blocks_create_enforcement_mark (C8 leftover)

HITL katalog trybu egzekucji bramy create per tenant. mark_code +
enforcement_kind block_409|warn_only|record_only|other + source_ref.
Nie live 409. Nie wiring create_block_mark.

## Dozwolone zależności
- `app.models.blocks_create_enforcement_mark`
- `app.repositories.blocks_create_enforcement_marks`
- `app.domain`

## Zakaz
- import innych BC services (create_block_marks, shipments, parties, charges)
- zapis `shipment` / `create_block_mark` / `party_document` / `charge`
- live 409 na POST shipment / wiring blocks_create / matching
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
