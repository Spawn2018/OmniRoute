# BC payment_terms_mark (EXP1)

HITL katalog warunków płatności per tenant. mark_code + terms_kind
net|prepaid|other + source_ref. Nie kolumna shipment. Nie payment_terms_days.

## Dozwolone zależności
- `app.models.payment_terms_mark`
- `app.repositories.payment_terms_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges, extraction, cash_discounts)
- zapis `shipment` / `party` / `charge` / `extraction_draft` / `cash_discount`
- kolumna payment_terms na shipment / party.payment_terms_days / skonto F2
- kwota / marża / float / score / days
- HTTP
- UPDATE / DELETE wiersza
