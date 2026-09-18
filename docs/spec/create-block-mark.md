# create_block_mark (C8 leftover)

## Fakt
- Tabela `create_block_mark`: organization_id, mark_code, block_kind (`block`|`warn`|`allow`|`other`), source_ref, created_at.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_create_block_marks`.
- API GET/POST `/create-block-marks`. UI `/create-block-marks`.

## Nie
- live 409 na shipment / egzekucja blocks_create / document_kind matching / kwota
