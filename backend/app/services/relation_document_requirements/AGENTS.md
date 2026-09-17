# BC relation_document_requirement (C8 leftover)

HITL katalog stancji wymogu dokumentow per rodzaj relacji. requirement_code +
relation_kind domestic|international|waste|other + source_ref. Nie 409. Nie matching.

## Dozwolone zależności
- `app.models.relation_document_requirement`
- `app.repositories.relation_document_requirements`
- `app.domain`

## Zakaz
- import innych BC services (party_documents, shipments, charges, extraction)
- zapis `party_document` / `shipment` / `charge` / `extraction_draft`
- 409 na POST shipment / blocks_create / document_kind matching
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
