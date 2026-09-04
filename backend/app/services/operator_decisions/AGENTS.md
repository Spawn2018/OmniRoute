# BC operator_decision (M-71)

Szyna Akceptuj/Zmień/Odrzuć per tenant. Lock po `lock_version`. Nie accept extractu 1.3, nie send.

## Dozwolone zależności
- `app.models.operator_decision`
- `app.repositories.operator_decisions`
- `app.domain`

## Zakaz
- import innych BC services (w tym inbound, quotations, extraction)
- zapis `rate_line` / `charge` / `quotation` / `inbound_message`
- liczenie kwot / marży / float
