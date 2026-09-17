# invoice_match_candidate (F10)

## Zakres
- Tabela `invoice_match_candidate`: organization_id, candidate_code, candidate_kind (`en`|`uss`|`epo`|`other`), source_ref, created_at.
- Append-only. RLS FORCE.
- API GET/POST `/invoice-match-candidates`. OpenFGA `can_manage_invoice_match_candidates`.
- UI `/invoice-match-candidates`.

## Poza
- live ranking SQL / książka EN+USS+EPO silnik / `postal_epo` / auto-link / kwota
