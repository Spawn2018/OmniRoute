# BC operator_notice (M-34)

Inbox powiadomień per tenant. Nie filtr wycen, nie send, nie outbox.

## Dozwolone zależności
- `app.models.operator_notice`
- `app.repositories.operator_notices`
- `app.domain`

## Zakaz
- import innych BC services (quotations, extraction, inbound)
- zapis `rate_line` / `charge` / `quotation`
- auto-INSERT z HITL / wyceny
- liczenie kwot / marży / float
