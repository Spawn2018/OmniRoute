# cargo_cover_mark (EXP2.4)

HITL katalog znacznika cargo cover per tenant. Nie live insurance. Nie polisa HTTP.

## Zakres

- Tabela `cargo_cover_mark`: organization_id, mark_code, cover_kind (`cargo`|`liability`|`policy`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/cargo-cover-marks`. OpenFGA `can_manage_cargo_cover_marks`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie kwota.

## Poza zakresem

- live insurance / polisa HTTP
- druga marża / float
- charge / HTTP
