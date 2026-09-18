# document_kind_match_mark (C8 leftover)

## Fakt
- Tabela `document_kind_match_mark`: organization_id, mark_code, match_kind (`block`|`warn`|`allow`|`other`), source_ref, created_at.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_document_kind_match_marks`.
- API GET/POST `/document-kind-match-marks`. UI `/document-kind-match-marks`.

## Nie
- live 409 na shipment / egzekucja blocks_create / document_kind matching / kwota
