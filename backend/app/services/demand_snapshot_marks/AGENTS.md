# BC demand_snapshot_mark (EXP3.13)

HITL katalog znacznika demand snapshot per tenant. mark_code + snapshot_kind
forecast|booking|actual|other + source_ref. Nie demand SQL. Nie auto-forecast.

## Dozwolone zaleznosci
- `app.models.demand_snapshot_mark`
- `app.repositories.demand_snapshot_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, inventory_position_marks)
- zapis `charge` / `extraction_draft` / `inventory_position_mark`
- demand SQL · auto-forecast · kwota
- HTTP
- UPDATE / DELETE wiersza
