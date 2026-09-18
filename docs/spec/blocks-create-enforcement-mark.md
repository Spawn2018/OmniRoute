# blocks_create_enforcement_mark (C8 leftover)

## Zakres

- Tabela `blocks_create_enforcement_mark`: organization_id, mark_code, enforcement_kind (`block_409`|`warn_only`|`record_only`|`other`), source_ref, created_at.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_blocks_create_enforcement_marks`.

## Poza zakresem

- live 409 na shipment / wiring blocks_create / mutacja create_block_mark / kwota
