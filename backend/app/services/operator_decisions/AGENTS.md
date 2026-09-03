# BC operator_decision (M-71)

Szyna Akceptuj/Odrzuć per tenant. Nie accept extractu 1.3, nie send, nie lock.

## Dozwolone zależności
- `app.models.operator_decision`
- `app.repositories.operator_decisions`
- `app.domain`

## Zakaz
- import innych BC services (w tym inbound, quotations, extraction)
- zapis `rate_line` / `charge` / `quotation` / `inbound_message`
- status `changed` w tym plasterze
- liczenie kwot / marży / float
