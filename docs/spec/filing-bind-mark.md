# filing_bind_mark (C1 leftover)

## Fakt
- Tabela `filing_bind_mark`: organization_id, mark_code, bind_kind (`shipment`|`scheme`|`both`|`other`), source_ref.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_filing_bind_marks`.
- API GET/POST `/filing-bind-marks`. UI `/filing-bind-marks`.

## Nie
- FK shipment/scheme · PUESC · SENT XML · kwota
