# BC outcome_kind (AI1.4)

HITL otwarty słownik rodzaju wyniku per tenant. kind_code + source_ref.
Nowy rodzaj = INSERT. Nie CHECK. Nie ENUM. Nie ledger.

## Dozwolone zależności
- `app.models.outcome_kind`
- `app.repositories.outcome_kinds`
- `app.domain`

## Zakaz
- import innych BC services (outcome_ledgers, suggestion_kinds, charges, extraction)
- zapis `outcome_ledger` / `suggestion_ledger` / `charge` / `extraction_draft`
- CHECK listy rodzajów / ENUM / FK z outcome_ledger
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
