# make_or_buy_mark (EXP2.2)

HITL katalog znacznika make-or-buy per tenant. Nie silnik. Nie koszt SQL.

## Zakres

- Tabela `make_or_buy_mark`: organization_id, mark_code, buy_kind (`make`|`buy`|`hybrid`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/make-or-buy-marks`. OpenFGA `can_edit`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie kwota. Nie allocation SQL.

## Poza zakresem

- Silnik make-or-buy / koszt allocation
- druga marża / float
- charge / HTTP

## Zależności

- F1 / charge (klej poza tym plastrem)
