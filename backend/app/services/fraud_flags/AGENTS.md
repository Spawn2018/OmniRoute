# BC fraud_flag (M-54)

Flaga oszustwa per tenant, FK do `party`. Nie kwota, nie scoring osoby, nie live lista.

## Dozwolone zależności
- `app.models.fraud_flag`
- `app.repositories.fraud_flags`
- `app.domain`

## Zakaz
- import innych BC services (parties, quotations, charges)
- zapis `party` / `quotation` / `charge` / `cargo_claim`
- kwoty / marża / float / scoring osoby
- HTTP
