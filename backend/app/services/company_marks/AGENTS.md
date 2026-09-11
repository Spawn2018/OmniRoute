# BC company_mark (G10)

HITL katalog znacznika spółki per tenant. mark_code + seat_kind hq|branch|other + source_ref. Nie drugi tenant. Nie company_id FK.

## Dozwolone zależności
- `app.models.company_mark`
- `app.repositories.company_marks`
- `app.domain`

## Zakaz
- import innych BC services (tenancy, charges, extraction, customer_contracts)
- zapis `organization` / `charge` / `app_user` / `customer_contract`
- drugi tenant / company_id FK / amount / ledger / float / kwota
- HTTP
- UPDATE / DELETE wiersza
