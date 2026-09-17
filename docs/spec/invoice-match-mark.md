# invoice_match_mark (F10 leftover)

## Zakres
- Tabela `invoice_match_mark`: organization_id, mark_code, match_kind (`candidate`|`rank`|`allocate`|`other`), source_ref, created_at.
- Append-only. RLS FORCE.
- API GET/POST `/invoice-match-marks`. OpenFGA `can_manage_invoice_match_marks`.
- UI `/invoice-match-marks`.

## Poza
- invoice_match_candidate / ranking SQL / purchase_invoice_allocation / auto-link / kwota
