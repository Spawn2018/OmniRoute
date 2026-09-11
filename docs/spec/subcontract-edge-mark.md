# subcontract_edge_mark (EXP2.6)

HITL katalog krawędzi podwykonawstwa per tenant. Nie live graph. Nie matching SQL.

## Zakres

- Tabela `subcontract_edge_mark`: organization_id, mark_code, edge_kind (`prime`|`sub`|`broker`|`other`), source_ref.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/subcontract-edge-marks`. OpenFGA `can_manage_subcontract_edge_marks`.
- UI lista + formularz.

## Poza zakresem

- live subcontract graph / matching SQL
- kwota / marża / float / HTTP
