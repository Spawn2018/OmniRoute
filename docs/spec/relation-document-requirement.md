# relation_document_requirement (C8)

## Zakres
- Tabela `relation_document_requirement`: organization_id, requirement_code, relation_kind (`en`|`uss`|`epo`|`other`), source_ref, created_at.
- Append-only. RLS FORCE.
- API GET/POST `/relation-document-requirements`. OpenFGA `can_manage_relation_document_requirements`.
- UI `/relation-document-requirements`.

## Poza
- live 409 na shipment / książka EN+USS+EPO silnik / `postal_epo` / blocks_create / kwota
