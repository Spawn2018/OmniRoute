# ais_import_mark (C2 leftover)

## Zakres

- Tabela `ais_import_mark`: organization_id, mark_code, import_kind (`ais`|`aes`|`intrastat`|`other`), source_ref, created_at.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_ais_import_marks`.

## Poza zakresem

- PUESC live / XML AIS/AES / Intrastat HTTP / kwota
