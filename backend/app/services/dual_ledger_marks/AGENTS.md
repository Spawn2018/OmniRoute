# BC dual_ledger_mark (EXP0.10)

HITL katalog znacznika dual ledger per tenant. mark_code + ledger_kind
ops|finance|tax|other + source_ref. Nie druga marża. Nie SQL na charge.

## Dozwolone zależności
- `app.models.dual_ledger_mark`
- `app.repositories.dual_ledger_marks`
- `app.domain`

## Zakaz
- import innych BC services (bookkeeping, entity_events, charges, extraction)
- zapis `bookkeeping` / `entity_event` / `charge` / `extraction_draft`
- druga marża / SQL na charge / JPK / ERP live
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
