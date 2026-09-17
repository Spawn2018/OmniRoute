# invoice_alloc_mark (F10 leftover)

## Zakres
- Tabela `invoice_alloc_mark`: organization_id, mark_code, alloc_kind (`line`|`header`|`batch`|`other`), source_ref, created_at.
- Append-only. RLS FORCE.
- API GET/POST `/invoice-alloc-marks`. OpenFGA `can_manage_invoice_alloc_marks`.
- UI `/invoice-alloc-marks`.

## Poza
- purchase_invoice_allocation / ranking SQL / invoice_match_candidate / auto-link / kwota
