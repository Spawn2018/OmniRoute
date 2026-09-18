# filing_fk_mark (C1 leftover)

## Zakres

- Tabela `filing_fk_mark`: organization_id, mark_code, fk_kind (`shipment`|`scheme`|`other`), source_ref, created_at.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_filing_fk_marks`.

## Poza zakresem

- live FK UUID / PUESC / SENT XML / kwota
