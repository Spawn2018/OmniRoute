# BC product_ticket (Plat-HD-flow)

HITL wpis ticketu produktu per tenant. ticket_code + title + body +
ticket_kind report|triage|owner_ok|other + source_ref. Nie auto-fix.
Nie CAPA. Nie FK mark.

## Dozwolone zależności
- `app.models.product_ticket`
- `app.repositories.product_tickets`
- `app.domain`

## Zakaz
- import innych BC services (product_ticket_marks, capa_marks, charges)
- zapis `product_ticket_mark` / `capa_mark` / `operator_notice` / `charge`
- auto-fix · agent PR · Mob Expo · FK mark
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
