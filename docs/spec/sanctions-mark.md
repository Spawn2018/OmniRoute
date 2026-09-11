# sanctions_mark (EXP2.5)

HITL katalog znacznika listy sankcji per tenant. Nie live scrape. Nie screening HTTP.

## Zakres

- Tabela `sanctions_mark`: organization_id, mark_code, list_kind (`ofac`|`eu`|`un`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/sanctions-marks`. OpenFGA `can_manage_sanctions_marks`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie kwota.

## Poza zakresem

- live sanctions scrape / OFAC HTTP
- druga marża / float
- charge / HTTP
