# cost_allocation_mark (EXP2.3)

HITL katalog znacznika cost allocation per tenant. Nie allocation SQL. Nie ABC silnik.

## Zakres

- Tabela `cost_allocation_mark`: organization_id, mark_code, alloc_kind (`direct`|`abc`|`shared`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/cost-allocation-marks`. OpenFGA `can_edit`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie kwota.

## Poza zakresem

- Allocation SQL / ABC engine
- druga marża / float
- charge / HTTP
