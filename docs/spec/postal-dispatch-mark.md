# postal_dispatch_mark (F11)

## Zakres
- Tabela `postal_dispatch_mark`: organization_id, mark_code, dispatch_kind (`en`|`uss`|`epo`|`other`), source_ref, created_at.
- Append-only. RLS FORCE.
- API GET/POST `/postal-dispatch-marks`. OpenFGA `can_manage_postal_dispatch_marks`.
- UI `/postal-dispatch-marks`.

## Poza
- live Poczta Polska / książka EN+USS+EPO silnik / `postal_epo` / e-Doręczenia / kwota
